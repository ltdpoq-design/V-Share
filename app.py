"""
share.vivi.homes - Flask 后端
小婷写的隐私分享服务 v3.0.0

v3.0.0:
- 六语言 i18n (en / zh-CN / zh-TW / ja / ko / es / fr)
- 重画 favicon (单 SVG 多尺寸)
- 服务端 API 错误文案本地化 (Accept-Language + ?lang=)
- /api/i18n/<lang> 暴露语言字典
- 新功能:
  - 设备标签（创建时记录）
  - 阅后即焚（burn_after_read）
  - 状态: active / burned / expired / soft-deleted
  - /api/version 返回版本号
"""
import os
import sqlite3
import uuid
import time
import json
import re
from flask import Flask, request, jsonify, send_from_directory, abort
import threading

# === 配置 ===
BASE_DIR = '/var/www/sites/shares'
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
DB_PATH = os.path.join(BASE_DIR, 'shares.db')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
MAX_TOTAL_SIZE = 5 * 1024 * 1024 * 1024  # 5 GB
EXPIRE_OPTIONS = {
    '10m': 10 * 60,
    '30m': 30 * 60,
    '1h': 60 * 60,
    '24h': 24 * 60 * 60,
    '48h': 48 * 60 * 60,
    '72h': 72 * 60 * 60,
}
SOFT_DELETE_DAYS = 30

# === 版本号 ===
APP_VERSION = '3.0.0'
APP_RELEASED = '2026-07-05'
APP_CHANGELOG = 'GLOBAL · NEON SVG · SIX LANGUAGES'

# === 支持的语言 ===
SUPPORTED_LANGS = ['en', 'zh-CN', 'zh-TW', 'ja', 'ko', 'es', 'fr']
DEFAULT_LANG = 'en'

# 简单 Accept-Language 解析（取 q 值最高的命中）
_ACCEPT_RE = re.compile(r'([a-zA-Z]{2,3}(?:-[a-zA-Z0-9]+)*)\s*(?:;\s*q\s*=\s*([0-9.]+))?', re.I)


def _parse_accept_language(header):
    """解析 Accept-Language 头，返回最佳匹配语言代码"""
    if not header:
        return None
    candidates = []
    for m in _ACCEPT_RE.finditer(header):
        tag = m.group(1)
        q_str = m.group(2)
        try:
            q = float(q_str) if q_str else 1.0
        except ValueError:
            q = 1.0
        # 规范化 (zh-cn → zh-CN)
        parts = tag.split('-')
        if len(parts) == 2:
            tag = parts[0].lower() + '-' + parts[1].upper()
        else:
            tag = tag.lower()
        candidates.append((q, tag))
    candidates.sort(key=lambda x: -x[0])
    for _, tag in candidates:
        if tag in SUPPORTED_LANGS:
            return tag
        # 主语言命中（如 zh 命中 zh-CN）
        primary = tag.split('-')[0].lower()
        for sl in SUPPORTED_LANGS:
            if sl.split('-')[0].lower() == primary:
                return sl
    return None


_I18N_CACHE = {}


def load_i18n(lang):
    """加载语言字典，缓存到内存"""
    if lang in _I18N_CACHE:
        return _I18N_CACHE[lang]
    path = os.path.join(STATIC_DIR, 'i18n', lang + '.json')
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        _I18N_CACHE[lang] = data
        return data
    except Exception:
        return None


def detect_lang():
    """根据 ?lang= > Accept-Language > 默认 确定语言"""
    q_lang = request.args.get('lang')
    if q_lang and q_lang in SUPPORTED_LANGS:
        return q_lang
    q_lang = request.form.get('lang')
    if q_lang and q_lang in SUPPORTED_LANGS:
        return q_lang
    header = request.headers.get('Accept-Language', '')
    parsed = _parse_accept_language(header)
    return parsed or DEFAULT_LANG


def t(key, lang=None):
    """查 i18n 字符串，找不到回退 en，再找不到回退 key 本身"""
    if lang is None:
        lang = detect_lang()
    data = load_i18n(lang)
    if data and key in data:
        return data[key]
    if lang != DEFAULT_LANG:
        data = load_i18n(DEFAULT_LANG)
        if data and key in data:
            return data[key]
    return key

os.makedirs(UPLOAD_DIR, exist_ok=True)
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE


# === 数据库 ===
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库表"""
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS shares (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                content TEXT,
                file_path TEXT,
                file_name TEXT,
                file_size INTEGER,
                mime_type TEXT,
                expires_at INTEGER NOT NULL,
                created_at INTEGER NOT NULL,
                deleted_at INTEGER,
                original_text TEXT,
                device TEXT,
                burn_after_read INTEGER DEFAULT 0,
                first_viewed_at INTEGER,
                burned_at INTEGER
            )
        ''')
        # 迁移: 旧表添加新字段
        cols = [r[1] for r in db.execute("PRAGMA table_info(shares)").fetchall()]
        for col, default in [('device', "'unknown'"), ('burn_after_read', '0'),
                             ('first_viewed_at', 'NULL'), ('burned_at', 'NULL')]:
            if col not in cols:
                try:
                    col_type = 'TEXT' if default.startswith("'") else 'INTEGER'
                    db.execute('ALTER TABLE shares ADD COLUMN ' + col + ' ' + col_type + ' DEFAULT ' + default)
                except Exception as e:
                    print('Migration ' + col + ': ' + str(e))
        db.commit()


# === 工具函数 ===
def get_total_size():
    total = 0
    if os.path.exists(UPLOAD_DIR):
        for f in os.listdir(UPLOAD_DIR):
            fp = os.path.join(UPLOAD_DIR, f)
            if os.path.isfile(fp):
                total += os.path.getsize(fp)
    return total


def mask_content(text, show_first=0):
    """
    对内容打码
    show_first=0: 全部 * (默认，已焚/过期用)
    show_first=2: 保留首 N 个字符 + * 中间屏蔽 (未读阅后即焚用)
    """
    if not text:
        return text
    if show_first > 0 and len(text) > show_first:
        return text[:show_first] + '*' * min(len(text) - show_first, 18)
    return '*' * min(len(text), 20)


def is_expired(expires_at):
    return int(time.time()) > expires_at


def get_status(row, now=None):
    """获取分享状态: active / burned / expired / soft-deleted"""
    if now is None:
        now = int(time.time())
    if row['burned_at']:
        return 'burned'
    if row['deleted_at']:
        return 'soft-deleted'
    if row['expires_at'] < now:
        return 'expired'
    return 'active'


# === 路由 ===
@app.route('/')
def index():
    with open(os.path.join(BASE_DIR, 'index.html'), 'r', encoding='utf-8') as f:
        return f.read()


@app.route('/api/version')
def version():
    lang = detect_lang()
    return jsonify({
        'version': APP_VERSION,
        'released': APP_RELEASED,
        'changelog': APP_CHANGELOG,
        'name': 'share.vivi.homes',
        'lang': lang,
        'supported_langs': SUPPORTED_LANGS,
    })


@app.route('/api/i18n/<lang>')
def get_i18n(lang):
    """返回指定语言字典（前端 fallback 用）"""
    if lang not in SUPPORTED_LANGS:
        lang = DEFAULT_LANG
    data = load_i18n(lang)
    if data is None:
        return jsonify({'error': 'lang_not_found', 'message': 'Language not found'}), 404
    return jsonify(data)


@app.route('/api/i18n')
def list_i18n():
    """返回支持的语种列表 + 元信息"""
    out = []
    for lang in SUPPORTED_LANGS:
        data = load_i18n(lang)
        meta = (data or {}).get('_meta', {})
        out.append({
            'code': lang,
            'name': meta.get('name', lang),
            'dir': meta.get('dir', 'ltr'),
        })
    return jsonify({
        'default': DEFAULT_LANG,
        'supported': out,
        'current': detect_lang(),
    })


@app.route('/api/share', methods=['POST'])
def create_share():
    current_size = get_total_size()
    if current_size >= MAX_TOTAL_SIZE:
        return jsonify({
            'error': 'storage_full',
            'message': t('error.storage_full')
        }), 507

    expire = request.form.get('expire', '72h')
    if expire not in EXPIRE_OPTIONS:
        expire = '72h'
    ttl = EXPIRE_OPTIONS[expire]
    expires_at = int(time.time()) + ttl

    share_id = uuid.uuid4().hex[:12]
    now = int(time.time())
    device = request.form.get('device', 'unknown')  # 新字段
    burn_after_read = 1 if request.form.get('burn_after_read') == '1' else 0  # 新字段

    share_type = 'text'
    content = None
    file_path = None
    file_name = None
    file_size = None
    mime_type = None

    if 'file' in request.files:
        f = request.files['file']
        if f and f.filename:
            ext = os.path.splitext(f.filename)[1]
            stored_name = share_id + ext
            stored_path = os.path.join(UPLOAD_DIR, stored_name)
            f.save(stored_path)
            file_size = os.path.getsize(stored_path)
            if get_total_size() > MAX_TOTAL_SIZE:
                os.remove(stored_path)
                return jsonify({
                    'error': 'storage_full',
                    'message': t('error.storage_full_file')
                }), 507
            file_path = stored_name
            file_name = f.filename
            mime_type = f.mimetype or 'application/octet-stream'
            share_type = 'file'

    if content is None:
        text = request.form.get('text', '').strip()
        if text:
            # URL 检测：在“网址”表单里前端会补协议；后端兜底补 http://
            text_lower = text.lower()
            first_token = text_lower.split()[0] if text_lower.split() else ''
            has_protocol = first_token.startswith(('http://', 'https://', 'ftp://'))
            has_scheme = '://' in first_token
            if not has_scheme:
                # 只要像 URL：域名/IP/localhost/带端口/含路径，都自动补 http://
                looks_like_url = (
                    first_token.startswith(('www.', 'localhost')) or
                    '.' in first_token or
                    ':' in first_token or
                    ('/' in first_token and ' ' not in first_token)
                )
                if looks_like_url:
                    text = 'http://' + text
                    text_lower = text.lower()
                    first_token = text_lower.split()[0]
                    has_protocol = True
                    has_scheme = True
            if has_protocol or has_scheme:
                share_type = 'url'
            else:
                share_type = 'text'
            content = text

    if share_type == 'text' and not content and not file_path:
        return jsonify({'error': 'empty', 'message': t('error.empty')}), 400

    with get_db() as db:
        db.execute('''
            INSERT INTO shares (id, type, content, file_path, file_name, file_size, mime_type, expires_at, created_at, original_text, device, burn_after_read)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (share_id, share_type, content, file_path, file_name, file_size, mime_type, expires_at, now, content, device, burn_after_read))
        db.commit()

    return jsonify({
        'id': share_id,
        'type': share_type,
        'expires_at': expires_at,
        'expires_in': ttl,
        'burn_after_read': bool(burn_after_read),
        'device': device,
        'url': f'https://share.vivi.homes/s/{share_id}'
    })


@app.route('/api/share/<share_id>')
def get_share(share_id):
    # 预览模式（不焚毁，只返回元信息）
    is_preview = request.args.get('preview') == '1'

    with get_db() as db:
        row = db.execute('SELECT * FROM shares WHERE id = ?', (share_id,)).fetchone()
        if not row:
            return jsonify({'error': 'not_found'}), 404

        now = int(time.time())
        expired = is_expired(row['expires_at'])
        status = get_status(row, now)

        # 阅后即焚 V3：第一次访问 = 立即焚毁 + 打码 + 删文件
        # 逻辑：用户读完后内容立刻消失，回到主页看到的状态就是"已焚"
        # 例外：preview 模式（警告页加载）不焚毁
        if (not is_preview) and status == 'active' and row['burn_after_read'] and not row['burned_at']:
            masked = mask_content(row['original_text']) if row['original_text'] else ''
            db.execute('UPDATE shares SET first_viewed_at = ?, burned_at = ?, content = ? WHERE id = ?',
                       (now, now, masked, share_id))
            db.commit()
            # 删除文件
            if row['file_path']:
                fp = os.path.join(UPLOAD_DIR, row['file_path'])
                if os.path.exists(fp):
                    try: os.remove(fp)
                    except: pass
            row = db.execute('SELECT * FROM shares WHERE id = ?', (share_id,)).fetchone()
            status = 'burned'

        # 过期软删除（第一次访问时）
        if expired and not row['deleted_at']:
            masked = mask_content(row['original_text']) if row['original_text'] else ''
            db.execute('UPDATE shares SET deleted_at = ?, content = ? WHERE id = ?', (now, masked, share_id))
            db.commit()
            if row['file_path']:
                fp = os.path.join(UPLOAD_DIR, row['file_path'])
                if os.path.exists(fp):
                    try: os.remove(fp)
                    except: pass
            row = db.execute('SELECT * FROM shares WHERE id = ?', (share_id,)).fetchone()
            status = 'soft-deleted'

        if status != 'active':
            return jsonify({
                'id': share_id,
                'status': status,
                'expired': True,
                'burned': status == 'burned',
                'type': row['type'],
                'content': row['content'],
                'file_name': row['file_name'],
                'file_path': row['file_path'],
                'file_size': row['file_size'],
                'mime_type': row['mime_type'],
                'expires_at': row['expires_at'],
                'created_at': row['created_at'],
                'burn_after_read': bool(row['burn_after_read']),
                'burned_at': row['burned_at'],
                'device': row['device'],
            })

        # active - 返回原文
        # active 状态
        response = {
            'id': share_id,
            'status': 'active',
            'expired': False,
            'burned': False,
            'type': row['type'],
            'file_name': row['file_name'],
            'file_path': row['file_path'],
            'file_size': row['file_size'],
            'mime_type': row['mime_type'],
            'expires_at': row['expires_at'],
            'created_at': row['created_at'],
            'burn_after_read': bool(row['burn_after_read']),
            'first_viewed_at': row['first_viewed_at'],
            'device': row['device'],
        }
        # preview 模式不返回 content（用户点确认后才真给）
        if not is_preview:
            response['content'] = row['content']
        else:
            response['preview'] = True
        return jsonify(response)


@app.route('/api/list')
def list_shares():
    """列出所有分享"""
    with get_db() as db:
        rows = db.execute(
            'SELECT id, type, content, file_name, file_size, mime_type, expires_at, created_at, deleted_at, device, burn_after_read, burned_at, first_viewed_at FROM shares ORDER BY created_at DESC LIMIT 50'
        ).fetchall()
        result = []
        now = int(time.time())
        for r in rows:
            d = dict(r)
            status = get_status(d, now)
            d['status'] = status
            d['burned'] = status == 'burned'
            # 已焚 / 已过期 → 全部 * 打码
            if status != 'active':
                if d.get('content'):
                    d['content'] = mask_content(d['content'])
                if d.get('file_name'):
                    d['file_name'] = mask_content(d['file_name'])
            elif d.get('burn_after_read') and not d.get('first_viewed_at') and not d.get('burned_at'):
                # 阅后即焚未读未焚：保留首 2 字 + * 中间屏蔽
                if d.get('content'):
                    d['content'] = mask_content(d['content'], show_first=2)
                if d.get('file_name'):
                    d['file_name'] = mask_content(d['file_name'], show_first=2)
            result.append(d)
        return jsonify(result)


@app.route('/api/stats')
def stats():
    with get_db() as db:
        now = int(time.time())
        total = db.execute('SELECT COUNT(*) FROM shares').fetchone()[0]
        active = db.execute('SELECT COUNT(*) FROM shares WHERE deleted_at IS NULL AND burned_at IS NULL AND expires_at > ?', (now,)).fetchone()[0]
        expired = db.execute('SELECT COUNT(*) FROM shares WHERE deleted_at IS NOT NULL').fetchone()[0]
        burned = db.execute('SELECT COUNT(*) FROM shares WHERE burned_at IS NOT NULL AND deleted_at IS NULL').fetchone()[0]
    return jsonify({
        'total': total,
        'active': active,
        'expired': expired,
        'burned': burned,
        'storage_used': get_total_size(),
        'storage_limit': MAX_TOTAL_SIZE,
        'storage_used_mb': round(get_total_size() / 1024 / 1024, 2),
        'storage_used_gb': round(get_total_size() / 1024 / 1024 / 1024, 2),
        'version': APP_VERSION,
    })


@app.route('/s/<share_id>')
def view_share(share_id):
    with open(os.path.join(BASE_DIR, 'view.html'), 'r', encoding='utf-8') as f:
        return f.read()


@app.route('/uploads/<filename>')
def download_file(filename):
    if '/' in filename or '..' in filename:
        abort(404)
    return send_from_directory(UPLOAD_DIR, filename, as_attachment=True)


@app.route('/static/<path:filename>')
def static_files(filename):
    """提供静态资源（favicon, manifest, etc）"""
    static_dir = os.path.join(BASE_DIR, 'static')
    return send_from_directory(static_dir, filename)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(BASE_DIR, 'static'), 'favicon.ico',
                                mimetype='image/x-icon')


@app.route('/favicon.svg')
def favicon_svg():
    return send_from_directory(os.path.join(BASE_DIR, 'static'), 'favicon.svg',
                               mimetype='image/svg+xml')


# === 后台清理线程 ===
def cleanup_old_shares():
    while True:
        try:
            with get_db() as db:
                threshold = int(time.time()) - SOFT_DELETE_DAYS * 24 * 60 * 60
                rows = db.execute('SELECT id, file_path FROM shares WHERE deleted_at IS NOT NULL AND deleted_at < ?', (threshold,)).fetchall()
                for row in rows:
                    if row['file_path']:
                        fp = os.path.join(UPLOAD_DIR, row['file_path'])
                        if os.path.exists(fp):
                            try: os.remove(fp)
                            except: pass
                # 也清理 30 天前已焚的（已焚的没 deleted_at，单独处理）
                burned_rows = db.execute('SELECT id, file_path FROM shares WHERE burned_at IS NOT NULL AND burned_at < ?', (threshold,)).fetchall()
                for row in burned_rows:
                    if row['file_path']:
                        fp = os.path.join(UPLOAD_DIR, row['file_path'])
                        if os.path.exists(fp):
                            try: os.remove(fp)
                            except: pass
                db.execute('DELETE FROM shares WHERE (deleted_at IS NOT NULL AND deleted_at < ?) OR (burned_at IS NOT NULL AND burned_at < ?)', (threshold, threshold))
                db.commit()
                if rows or burned_rows:
                    print(f'[CLEANUP] Removed {len(rows) + len(burned_rows)} old shares (30+ days)')
        except Exception as e:
            print(f'[CLEANUP] Error: {e}')
        time.sleep(3600)


if __name__ == '__main__':
    init_db()
    cleanup_thread = threading.Thread(target=cleanup_old_shares, daemon=True)
    cleanup_thread.start()
    app.run(host='127.0.0.1', port=5001, debug=False)