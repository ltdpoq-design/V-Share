<div align="center">

# 🔗 V Share

### 链接来过，痕迹不必留下。

**一个极简、无需注册、跨设备的文本与文件分享工具。**
粘贴文字、拖入文件，立刻得到一个可分享的链接，发给对方用浏览器直接打开就行，不用装客户端。

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md)

</div>

---

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version v3.0.0](https://img.shields.io/badge/version-v3.0.0-blue.svg)](CHANGELOG.md)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-yellow.svg)](requirements.txt)
[![Languages](https://img.shields.io/badge/i18n-7%20languages-purple.svg)](#-多语言)
[![Live Demo](https://img.shields.io/badge/demo-share.vivi.homes-ff69b4.svg)](https://share.vivi.homes)

> 🌐 在线演示：**<https://share.vivi.homes>**
> 📦 仓库地址：**<https://github.com/ltdpoq-design/V-Share>**
> 📝 发布说明：[v3.0.0（2026-07-05）](https://github.com/ltdpoq-design/V-Share/releases/tag/v3.0.0)

---

## ✨ 功能亮点

- 🌍 **原生支持 7 种语言** — English（默认）、简体中文、繁體中文、日本語、한국어、Español、Français，右上角一键切换，偏好保存在 `localStorage`，下次打开还是它。
- 🔥 **阅后即焚** — 链接被打开一次后立即销毁，接收方只看到一次。
- 🎨 **霓虹 Favicon** — 单个 `favicon.svg` 自动缩放，16 px 到 256 px 都清晰，再也不糊。
- 🏷️ **分享自带设备标签** — 创建时自动记录发起设备，方便追溯来源。
- 📊 **完整的分享生命周期** — `active` / `burned` / `expired` / `soft-deleted`，状态清晰，不再黑盒。
- 🔒 **零注册、零追踪** — 不要邮箱、不要手机号、不要 Cookie。
- 📝 **文字 + 文件双通道** — 短文、代码片段、图片、PDF，单文件上限 **100 MB**。
- 🔗 **链接自动补全** — 粘贴 `github.com/...` 自动变成 `https://github.com/...`。
- ▶️ **YouTube 增强** — 自动展开为可嵌入播放器，集成 SponsorBlock 自动跳过广告。
- ⏱ **灵活时效** — `10m / 30m / 1h / 24h / 48h / 72h`，随时可手动删。
- 🧯 **软删除保留 30 天** — 误删 30 天内可恢复，到期自动清理。
- 📡 **API 优先** — 每个界面功能同时也是 REST 接口，方便写脚本。

## 🚀 快速开始

需要 **Python 3.11+**。

```bash
# 1. 克隆
git clone https://github.com/ltdpoq-design/V-Share.git
cd V-Share

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动（默认监听 0.0.0.0:5001）
python3 app.py
```

浏览器打开 <http://localhost:5001>，拖个文件或粘段文字 → 点「分享」→ 复制链接 → 发给朋友。

### 生产部署（Gunicorn）

```bash
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:5001 app:app
```

## 🌐 多语言

V Share 在 `static/i18n.js` 和 `static/i18n/` 下准备好了完整的本地化层。**右上角的语言菜单**可以切换 7 种语言，切换结果会记到浏览器的 `localStorage`（键名 `vshare.lang`），下次再来还是你的选择。

### 支持的语言

| 语言代码 | 语言         |
| -------- | ------------ |
| `en`     | English      |
| `zh-CN`  | 简体中文     |
| `zh-TW`  | 繁體中文     |
| `ja`     | 日本語       |
| `ko`     | 한국어       |
| `es`     | Español      |
| `fr`     | Français     |

### 通过 API 拉翻译表

```bash
# 拉所有支持的语言
curl https://share.vivi.homes/api/i18n

# 拉英文翻译表
curl https://share.vivi.homes/api/i18n/en
```

## 🔌 API 接口

| 方法     | 路径                         | 说明                          |
| -------- | ---------------------------- | ----------------------------- |
| `POST`   | `/api/share`                 | 创建文本或文件分享            |
| `GET`    | `/api/share/<id>`            | 读取分享（阅后即焚会计数一次）|
| `DELETE` | `/api/share/<id>`            | 软删除分享                    |
| `GET`    | `/api/list`                  | 列出全部分享及其元数据        |
| `GET`    | `/api/stats`                 | 聚合统计                      |
| `GET`    | `/api/version`               | 服务版本（`v3.0.0`）          |
| `GET`    | `/api/i18n`                  | 支持的语言列表                |
| `GET`    | `/api/i18n/<lang>`           | 单语言翻译表                  |
| `GET`    | `/s/<id>`                    | 短链跳转查看页                |
| `GET`    | `/uploads/&lt;filename&gt;`  | 下载已上传文件                |

> 🔔 详细的请求/响应字段在 `app.py` 各路由的内嵌注释里。

## 🌍 部署

### Nginx 反向代理示例

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

**生产环境务必在反代前面挂一层 HTTPS**（Let's Encrypt / Caddy / Cloudflare 都可以）。

## 🛡 安全建议

- 上线一定要走 HTTPS，不要裸跑 HTTP。
- 生产用 Gunicorn + systemd，别用 Flask 自带的 dev server。
- 定期备份 `shares.db`，里面是全量分享历史。
- 监控 `uploads/` 目录大小，必要时写脚本清理过期文件。
- 公开部署建议加一层速率限制（Nginx `limit_req` 或者 WAF）。

## 📁 目录结构

```
.
├── app.py               # Flask 后端（单文件）
├── index.html           # 创建分享页面
├── view.html            # 查看分享页面
├── static/
│   ├── favicon.svg      # 霓虹 Favicon（单 SVG，全尺寸自适应）
│   ├── i18n.js          # 客户端多语言加载器
│   └── i18n/            # 翻译表（en / zh-CN / zh-TW / ja / ko / es / fr）
├── uploads/             # 运行时上传目录（已 gitignore）
├── requirements.txt
├── LICENSE
└── README.md            # ← 你正在看这个
```

## 📄 开源协议

[MIT](LICENSE) 协议，随便用，欢迎注明出处。

---

<div align="center">

<sub>v3.0.0 · 2026-07-05 · *NEON DROP · ZERO TRACE · ONE TAP SHARE*</sub>

</div>
