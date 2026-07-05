<div align="center">

# 🔗 V Share

### 連結送達，痕跡不必留下。

**極簡、免註冊、跨裝置的文字與檔案分享小工具。**
貼上文字或拖入檔案，立刻產生分享連結；對方用瀏覽器直接開啟，無需安裝任何用戶端。

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md)

</div>

---

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![版本 v3.0.0](https://img.shields.io/badge/%E7%89%88%E6%9C%AC-v3.0.0-blue.svg)](CHANGELOG.md)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-yellow.svg)](requirements.txt)
[![多語系](https://img.shields.io/badge/i18n-7%20%E7%A8%AE%E8%AA%9E%E8%A8%80-purple.svg)](#-多語系)

> 📦 程式碼倉庫：**<https://github.com/ltdpoq-design/V-Share>**
> 📝 版本發佈說明：[v3.0.0（2026-07-05）](https://github.com/ltdpoq-design/V-Share/releases/tag/v3.0.0)

---

## ✨ 功能特色

- 🌍 **內建 7 種語言** — English（預設）、簡體中文、繁體中文、日本語、한국어、Español、Français，右上角下拉選單一鍵切換，紀錄寫進 `localStorage`，下次來還是您的選擇。
- 🔥 **閱後即焚** — 連結被打開一次就立即銷毀，對方只看得到一次。
- 🎨 **霓虹 Favicon** — 單一 `favicon.svg` 自動縮放，16 px 到 256 px 都銳利，不再糊成一團。
- 🏷️ **分享自帶裝置標籤** — 建立時自動記錄發起端的裝置名稱，方便日後追溯。
- 📊 **完整的分享生命週期** — `active` / `burned` / `expired` / `soft-deleted`，狀態明確不再黑箱。
- 🔒 **免註冊、免追蹤** — 不留 Email、不留電話、不強塞 Cookie。
- 📝 **文字 + 檔案雙通道** — 短文、程式碼片段、圖片、PDF，單檔上限 **100 MB**。
- 🔗 **連結自動補全** — 貼上 `github.com/...` 會自動補成 `https://github.com/...`。
- ▶️ **YouTube 強化** — 自動展開為嵌入式播放器，整合 SponsorBlock 自動跳過業配片段。
- ⏱ **彈性時效** — 提供 `10m / 30m / 1h / 24h / 48h / 72h`，也可隨時手動刪除。
- 🧯 **30 天軟刪除保留** — 不小心刪掉的 30 天內可還原，之後自動清理。
- 📡 **API 優先** — 每個畫面功能也開放成 REST 端點，方便串接腳本。

## 🚀 快速開始

需要 **Python 3.11+**。

```bash
# 1. 複製專案
git clone https://github.com/ltdpoq-design/V-Share.git
cd V-Share

# 2. 安裝相依套件
pip install -r requirements.txt

# 3. 啟動服務（預設監聽 0.0.0.0:5001）
python3 app.py
```

打開瀏覽器連到 <http://localhost:5001>，拖檔案或貼段文字 → 按下「分享」→ 複製連結 → 傳給對方。

### 正式環境（Gunicorn）

```bash
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:5001 app:app
```

## 🌐 多語系

V Share 在 `static/i18n.js` 與 `static/i18n/` 提供完整的在地化機制。**畫面右上角的語言切換選單**可以挑選 7 種語言，選擇會以 `localStorage`（鍵名 `vshare.lang`）保存在使用者瀏覽器中。

### 支援的語系

| 語系代碼 | 語言         |
| -------- | ------------ |
| `en`     | English      |
| `zh-CN`  | 简体中文     |
| `zh-TW`  | 繁體中文     |
| `ja`     | 日本語       |
| `ko`     | 한국어       |
| `es`     | Español      |
| `fr`     | Français     |

### 透過 API 取得翻譯表

```bash
# 取得所有支援的語系
curl http://127.0.0.1:5001/api/i18n

# 取得繁體中文翻譯表
curl http://127.0.0.1:5001/api/i18n/zh-TW
```

## 🔌 API 一覽

| 方法     | 路徑                         | 說明                              |
| -------- | ---------------------------- | --------------------------------- |
| `POST`   | `/api/share`                 | 建立文字或檔案分享                |
| `GET`    | `/api/share/<id>`            | 讀取分享（閱後即焚會計數一次）    |
| `DELETE` | `/api/share/<id>`            | 軟刪除分享                        |
| `GET`    | `/api/list`                  | 列出分享與其後設資料              |
| `GET`    | `/api/stats`                 | 彙總統計                          |
| `GET`    | `/api/version`               | 服務版本（`v3.0.0`）              |
| `GET`    | `/api/i18n`                  | 支援的語系清單                    |
| `GET`    | `/api/i18n/<lang>`           | 取得單一語系翻譯表                |
| `GET`    | `/s/<id>`                    | 短網址跳轉到查看頁                |
| `GET`    | `/uploads/&lt;filename&gt;`  | 下載已上傳檔案                    |

> 🔔 詳細的請求／回應欄位都寫在 `app.py` 各路由的註解裡。

## 🌍 部署

### Nginx 反向代理範例

```nginx
server {
    listen 80;
    server_name share.example.com;

    client_max_body_size 100M;  # 與 MAX_FILE_SIZE 保持一致

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

**正式環境請務必在反代之前再加一層 HTTPS**（Let's Encrypt / Caddy / Cloudflare 都可）。

## 🛡 安全建議

- 對外服務務必走 HTTPS。
- 正式環境建議改用 Gunicorn + systemd，而非 Flask 內建的開發伺服器。
- `shares.db` 內含所有分享歷史，請定期備份。
- 注意 `uploads/` 目錄大小，必要時寫腳本清理過期檔案。
- 公開部署建議加上速率限制（Nginx `limit_req` 或 WAF）。

## 📁 專案結構

```
.
├── app.py               # Flask 後端（單檔）
├── index.html           # 建立分享頁
├── view.html            # 查看分享頁
├── static/
│   ├── favicon.svg      # 霓虹 Favicon（單 SVG，全尺寸適用）
│   ├── i18n.js          # 客戶端 i18n 載入器
│   └── i18n/            # 翻譯表（en / zh-CN / zh-TW / ja / ko / es / fr）
├── uploads/             # 執行時上傳目錄（已加入 .gitignore）
├── requirements.txt
├── LICENSE
└── README.md            # ← 您正在閱讀此檔
```

## 📄 授權條款

採用 [MIT](LICENSE) 授權，歡迎自由使用，標明出處我們會很開心。

---

<div align="center">

<sub>v3.0.0 · 2026-07-05 · *NEON DROP · ZERO TRACE · ONE TAP SHARE*</sub>

</div>
