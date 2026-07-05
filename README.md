# V Share

> A minimalist cross-device content & file sharing tool.

V Share 是一个轻量、零注册的跨设备内容与文件分享工具。打开网页，粘贴文字或拖入文件，立刻生成一个可分享的链接；接收方在浏览器中直接查看，无需安装任何客户端。

## ✨ 功能亮点

- **零注册 / 零登录** — 打开即用，不留账号、不留邮箱
- **文本与文件双通道** — 短文、代码片段、图片、PDF 任意分享，单文件最大 100 MB
- **链接自动补全** — 粘贴纯文本域名（如 `github.com`）会自动补全为 `https://github.com`
- **YouTube 增强** — 自动展开为可嵌入播放器，支持 SponsorBlock 跳过广告/赞助片段
- **阅后即焚（burn after read）** — 接收方访问一次后立即销毁
- **设备标签** — 创建分享时记录发起设备，便于追溯
- **自动过期** — 支持 10m / 30m / 1h / 24h / 48h / 72h 多种时效
- **状态管理** — `active` / `burned` / `expired` / `soft-deleted` 全生命周期
- **软删除保留 30 天** — 误删可恢复，过期自动清理
- **响应式前端** — 桌面 / 平板 / 手机自适应
- **API 优先** — 全部功能均提供 RESTful API，便于集成
- **单文件部署** — 后端 `app.py` 一个文件，SQLite 存储，开箱即用

## 📦 部署

### 环境要求

- Python **3.11+**（开发与测试版本为 3.11）
- pip
- （可选）Nginx / Apache 做反向代理与 HTTPS 终结

### 安装与启动

```bash
# 1. 克隆仓库
git clone https://github.com/ltdpoq-design/V-Share.git
cd V-Share

# 2. 安装依赖
pip install -r requirements.txt

# 3. （可选）创建 .env 自定义配置
cp .env.example .env   # 如果项目提供了示例；当前版本直接修改 app.py 顶部常量

# 4. 启动
python3 app.py
# 默认监听 http://0.0.0.0:5001
```

### 生产环境（Gunicorn）

```bash
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:5001 app:app
```

### 反向代理示例（Nginx）

```nginx
server {
    listen 80;
    server_name share.example.com;

    client_max_body_size 100M;  # 与 MAX_FILE_SIZE 保持一致

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }
}
```

### 反向代理示例（Apache）

```apache
<VirtualHost *:80>
    ServerName share.example.com

    ProxyPreserveHost On
    ProxyRequests Off
    RequestHeader set X-Forwarded-Proto "http"

    ProxyPass        / http://127.0.0.1:5001/ retry=0
    ProxyPassReverse / http://127.0.0.1:5001/

    # 允许 100MB 上传
    LimitRequestBody 104857600
</VirtualHost>
```

### HTTPS

强烈建议在反代前置一层 HTTPS（Let's Encrypt / Caddy / Cloudflare 等）。

## ⚙️ 配置项

`app.py` 顶部集中定义了所有可调常量：

| 常量 | 默认值 | 说明 |
| --- | --- | --- |
| `BASE_DIR` | `/var/www/sites/shares` | 项目根目录（部署时需修改） |
| `UPLOAD_DIR` | `<BASE_DIR>/uploads` | 上传文件存储目录 |
| `DB_PATH` | `<BASE_DIR>/shares.db` | SQLite 数据库路径 |
| `MAX_FILE_SIZE` | `100 * 1024 * 1024` (100 MB) | 单文件大小上限 |
| `MAX_TOTAL_SIZE` | `5 * 1024**3` (5 GB) | 全部分享累计大小上限 |
| `EXPIRE_OPTIONS` | `10m/30m/1h/24h/48h/72h` | 可选的过期时长 |
| `SOFT_DELETE_DAYS` | `30` | 软删除保留天数 |
| `APP_VERSION` | `2.9.2` | 当前版本号 |

修改后重启服务即可生效。

## 🔌 API 概览

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| `POST` | `/api/share` | 创建文本 / 文件分享 |
| `GET`  | `/api/share/<id>` | 获取分享内容 |
| `DELETE` | `/api/share/<id>` | 删除（软删除）分享 |
| `GET`  | `/api/version` | 获取服务版本号 |
| `GET`  | `/` | 主页（`index.html`） |
| `GET`  | `/view/<id>` | 查看页（`view.html`） |
| `GET`  | `/uploads/<filename>` | 下载已上传文件 |

详细参数参见 `app.py` 中各路由注释。

## 🗂 目录结构

```
.
├── app.py            # Flask 后端（单文件）
├── index.html        # 主页面（创建分享）
├── view.html         # 查看页面（接收分享）
├── static/           # 静态资源（favicon / PWA 图标）
├── uploads/          # 运行时上传的文件（.gitkeep 占位，不入库）
├── requirements.txt  # Python 依赖
├── LICENSE           # MIT 协议
└── README.md         # 本文件
```

## 🛡 安全建议

- **务必**部署在反代之后并启用 HTTPS
- 生产环境建议改用 Gunicorn + systemd 托管，而非 Flask 自带 dev server
- 定期备份 `shares.db`（包含所有历史分享）
- 监控 `uploads/` 目录大小，必要时触发自动清理任务
- 若对外公开，建议接入速率限制（如 Nginx `limit_req`）

## 🧭 版本

当前版本：**v2.9.2** · 发布日期 2026-06-30 · 代号 *NEON DROP · ZERO TRACE · ONE TAP SHARE*

## 📄 License

本项目基于 [MIT License](LICENSE) 开源。