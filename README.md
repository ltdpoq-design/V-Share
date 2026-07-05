<div align="center">

# 🔗 V Share

### Link arrives. No traces remain.

**A minimalist, zero-account, cross-device content & file sharing tool.**
Paste text or drop a file, get a shareable link, send it to anyone — works in any browser, no client install.

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md)

</div>

---

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version v3.0.0](https://img.shields.io/badge/version-v3.0.0-blue.svg)](CHANGELOG.md)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-yellow.svg)](requirements.txt)
[![Languages](https://img.shields.io/badge/i18n-7%20languages-purple.svg)](#-languages--i18n)

> 📦 Repository: **<https://github.com/ltdpoq-design/V-Share>**
> 📝 Release notes: [v3.0.0 (2026-07-05)](https://github.com/ltdpoq-design/V-Share/releases/tag/v3.0.0)

---

## ✨ Features

- 🌍 **Seven languages out of the box** — English (default), 简体中文, 繁體中文, 日本語, 한국어, Español, Français — switch with one click, persisted in `localStorage`.
- 🔥 **Burn-after-read** — a share can self-destruct after the first view, so the recipient gets exactly one peek.
- 🎨 **Neon favicon** — a single `favicon.svg` scales crisply from 16 px to 256 px; no more raster blur.
- 🏷️ **Per-share device tags** — every share records the originating device label, so you can trace where a piece of content came from.
- 📊 **Explicit share lifecycle** — `active` → `burned` / `expired` / `soft-deleted` instead of vague "deleted" flags.
- 🔒 **Zero account, zero tracking** — no email, no phone, no cookies required.
- 📝 **Text or file** — short notes, code snippets, images, PDFs; per-file cap **100 MB**.
- 🔗 **Smart link expansion** — paste `github.com/…` and it becomes a clickable `https://github.com/…`.
- ▶️ **YouTube enhancement** — auto-embeds a player with SponsorBlock to skip sponsor segments.
- ⏱ **Flexible expiry** — `10m / 30m / 1h / 24h / 48h / 72h`, plus a manual delete.
- 🧯 **30-day soft delete** — accidental deletes are recoverable for 30 days before permanent purge.
- 📡 **API-first** — every UI feature is also a REST endpoint, ready for scripting.

## 🚀 Quick Start

Requires **Python 3.11+**.

```bash
# 1. Clone
git clone https://github.com/ltdpoq-design/V-Share.git
cd V-Share

# 2. Install
pip install -r requirements.txt

# 3. Run (binds 0.0.0.0:5001 by default)
python3 app.py
```

Then open <http://localhost:5001>. Drop a file or paste text → click **Share** → copy the link → send it to anyone.

### Production (Gunicorn)

```bash
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:5001 app:app
```

## 🌐 Languages / i18n

V Share ships with a first-class localization layer in `static/i18n.js` and seven JSON tables under `static/i18n/`. The **language switcher in the top-right corner** lets visitors pick any of the seven supported languages; the choice persists per browser via `localStorage` (`vshare.lang`).

### Supported locales

| Code   | Language        |
| ------ | --------------- |
| `en`   | English         |
| `zh-CN`| 简体中文         |
| `zh-TW`| 繁體中文         |
| `ja`   | 日本語          |
| `ko`   | 한국어           |
| `es`   | Español         |
| `fr`   | Français        |

### Fetch translation tables (API)

```bash
# Returns the language list
curl http://127.0.0.1:5001/api/i18n

# Returns the English table
curl http://127.0.0.1:5001/api/i18n/en
```

## 🔌 API

| Method   | Path                       | Description                                  |
| -------- | -------------------------- | -------------------------------------------- |
| `POST`   | `/api/share`               | Create a text or file share                  |
| `GET`    | `/api/share/<id>`          | Retrieve a share (counts a burn-after-read)  |
| `DELETE` | `/api/share/<id>`          | Soft-delete a share                          |
| `GET`    | `/api/list`                | List shares with metadata                     |
| `GET`    | `/api/stats`               | Aggregate stats                               |
| `GET`    | `/api/version`             | Server version (`v3.0.0`)                     |
| `GET`    | `/api/i18n`                | Available language list                       |
| `GET`    | `/api/i18n/<lang>`         | Translation table for `<lang>`               |
| `GET`    | `/s/<id>`                  | Short URL → view page                         |
| `GET`    | `/uploads/&lt;filename&gt;`| Download an uploaded file                     |

> 🔔 Full request/response schemas live as inline comments in `app.py`.

## 🌍 Deploy

### Nginx reverse proxy

```nginx
server {
    listen 80;
    server_name share.example.com;

    client_max_body_size 100M;  # keep in sync with MAX_FILE_SIZE

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

Put **HTTPS** (Let's Encrypt / Caddy / Cloudflare) in front of the proxy.

## 🛡 Security Notes

- Always run behind HTTPS in production.
- Prefer Gunicorn + systemd over Flask's dev server.
- Snapshot `shares.db` regularly — it holds every share's history.
- Watch `uploads/` size and add a janitor for stale files.
- Public deployments should add rate limiting (Nginx `limit_req` or a WAF).

## 📁 Project Layout

```
.
├── app.py               # Flask backend (single file)
├── index.html           # Create-share page
├── view.html            # Receive-share page
├── static/
│   ├── favicon.svg      # Neon favicon (single SVG, all sizes)
│   ├── i18n.js          # Client-side i18n loader
│   └── i18n/            # Translation tables (en, zh-CN, zh-TW, ja, ko, es, fr)
├── uploads/             # Runtime uploads (gitignored)
├── requirements.txt
├── LICENSE
└── README.md            # ← you are here
```

## 📄 License

[MIT](LICENSE) — do whatever you like, attribution appreciated.

---

<div align="center">

<sub>v3.0.0 · 2026-07-05 · *NEON DROP · ZERO TRACE · ONE TAP SHARE*</sub>

</div>
