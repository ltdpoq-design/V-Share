<div align="center">

# 🔗 V Share

### リンクは届く、痕跡は残らない。

**ミニマルで登録不要、端末を問わないテキスト／ファイル共有ツールです。**
テキストを貼り付けるか、ファイルをドロップすれば共有リンクが即座に発行されます。受け側はブラウザで開くだけ、クライアントソフトのインストールは不要です。

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md)

</div>

---

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version v3.0.0](https://img.shields.io/badge/version-v3.0.0-blue.svg)](CHANGELOG.md)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-yellow.svg)](requirements.txt)
[![Languages](https://img.shields.io/badge/i18n-7%20languages-purple.svg)](#-対応言語--i18n)
[![Live Demo](https://img.shields.io/badge/demo-share.vivi.homes-ff69b4.svg)](https://share.vivi.homes)

> 🌐 ライブデモ：**<https://share.vivi.homes>**
> 📦 リポジトリ：**<https://github.com/ltdpoq-design/V-Share>**
> 📝 リリースノート：[v3.0.0（2026-07-05）](https://github.com/ltdpoq-design/V-Share/releases/tag/v3.0.0)

---

## ✨ 主な機能

- 🌍 **7 言語を標準搭載** — English（既定）、简体中文、繁體中文、日本語、韓国語（한국어）、Español、Français。右上のメニューからワンクリックで切り替えられ、選択は `localStorage` に保存されます。
- 🔥 **閲覧後自動消去（burn-after-read）** — 共有リンクを一度開くと即座に削除され、受信者は 1 回だけ閲覧できます。
- 🎨 **ネオン仕様の Favicon** — 単一の `favicon.svg` が 16 px から 256 px まで自動でスケール。ラスターのボヤけはもうありません。
- 🏷️ **共有ごとの端末タグ** — 作成時に発信元のデバイス名を記録し、後から出所をたどれます。
- 📊 **分かりやすいライフサイクル** — `active` / `burned` / `expired` / `soft-deleted` の状態を明示し、曖昧な「削除フラグ」は撤廃しました。
- 🔒 **アカウント登録ゼロ、追跡ゼロ** — メールアドレス、電話番号、Cookie は不要です。
- 📝 **テキストとファイルの二刀流** — メモ、コード断片、画像、PDF に対応。1 ファイルあたり **100 MB** まで。
- 🔗 **リンクの自動補完** — `github.com/...` を貼り付けると自動で `https://github.com/...` に展開されます。
- ▶️ **YouTube 拡張** — 貼り付けた URL を埋め込みプレイヤーに自動展開し、SponsorBlock でスポンサー部分をスキップします。
- ⏱ **柔軟な有効期限** — `10分 / 30分 / 1時間 / 24時間 / 48時間 / 72時間` に加え、手動削除も可能です。
- 🧯 **30 日の論理削除保持** — うっかり削除しても 30 日以内なら復元でき、期限後は自動クリーンアップされます。
- 📡 **API ファースト設計** — すべての UI 機能を REST API でも提供しており、スクリプト連携が容易です。

## 🚀 はじめてみよう

**Python 3.11 以上**が必要です。

```bash
# 1. リポジトリを取得
git clone https://github.com/ltdpoq-design/V-Share.git
cd V-Share

# 2. 依存関係をインストール
pip install -r requirements.txt

# 3. サーバーを起動（既定で 0.0.0.0:5001 で待ち受け）
python3 app.py
```

ブラウザで <http://localhost:5001> を開き、ファイルをドロップするかテキストを貼り付けて →「Share」をクリック → 表示されたリンクをコピーして送ってください。

### 本番運用（Gunicorn）

```bash
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:5001 app:app
```

## 🌐 対応言語 / i18n

V Share は `static/i18n.js` と `static/i18n/` 配下の 7 つの JSON テーブルで完全なローカライズ層を提供します。**画面右上の言語スイッチャー**から 7 言語を切り替えられ、選択は `localStorage`（キー名 `vshare.lang`）に記録されます。

### 対応ロケール

| コード    | 言語         |
| --------- | ------------ |
| `en`      | English      |
| `zh-CN`   | 简体中文     |
| `zh-TW`   | 繁體中文     |
| `ja`      | 日本語       |
| `ko`      | 한국어       |
| `es`      | Español      |
| `fr`      | Français     |

### API で翻訳テーブルを取得

```bash
# 対応言語の一覧を取得
curl https://share.vivi.homes/api/i18n

# 日本語の翻訳テーブルを取得
curl https://share.vivi.homes/api/i18n/ja
```

## 🔌 API

| メソッド  | パス                          | 概要                                         |
| --------- | ----------------------------- | -------------------------------------------- |
| `POST`    | `/api/share`                  | テキスト／ファイルの共有を新規作成           |
| `GET`     | `/api/share/<id>`             | 共有を取得（閲覧後消去は 1 回とカウント）    |
| `DELETE`  | `/api/share/<id>`             | 共有を論理削除                               |
| `GET`     | `/api/list`                   | 共有とそのメタデータの一覧                   |
| `GET`     | `/api/stats`                  | 集計統計                                     |
| `GET`     | `/api/version`                | サーバーバージョン（`v3.0.0`）               |
| `GET`     | `/api/i18n`                   | 対応言語の一覧                               |
| `GET`     | `/api/i18n/<lang>`            | 指定言語の翻訳テーブル                       |
| `GET`     | `/s/<id>`                     | 短縮 URL → 表示ページへ                      |
| `GET`     | `/uploads/&lt;filename&gt;`   | アップロード済みファイルのダウンロード       |

> 🔔 リクエスト／レスポンスの詳細は `app.py` の各ルート内コメントに記載しています。

## 🌍 デプロイ

### Nginx リーバスプロキシの例

```nginx
server {
    listen 80;
    server_name share.example.com;

    client_max_body_size 100M;  # MAX_FILE_SIZE と揃えてください

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

本番運用では **HTTPS**（Let's Encrypt / Caddy / Cloudflare など）をプロキシ前面に必ず配置してください。

## 🛡 セキュリティに関する注意

- 本番では必ず HTTPS 経由で配信してください。
- Flask の開発サーバーではなく、Gunicorn + systemd での運用を推奨します。
- `shares.db` は全共有履歴を含むため、定期的にバックアップを取ってください。
- `uploads/` のディスク使用量を監視し、不要ファイルを掃除する仕組みを用意してください。
- 公開運用ではレートリミット（Nginx の `limit_req` や WAF）の導入を推奨します。

## 📁 ディレクトリ構成

```
.
├── app.py               # Flask バックエンド（単一ファイル）
├── index.html           # 共有作成ページ
├── view.html            # 共有閲覧ページ
├── static/
│   ├── favicon.svg      # ネオン Favicon（単一 SVG、全サイズ対応）
│   ├── i18n.js          # クライアント側 i18n ローダー
│   └── i18n/            # 翻訳テーブル（en / zh-CN / zh-TW / ja / ko / es / fr）
├── uploads/             # ランタイムのアップロード先（.gitignore 対象）
├── requirements.txt
├── LICENSE
└── README.md            # ← いま読んでいるこのファイル
```

## 📄 ライセンス

[MIT](LICENSE) ライセンスの下で公開しています。自由にご利用ください、出典を添えていただけると嬉しいです。

---

<div align="center">

<sub>v3.0.0 · 2026-07-05 · *NEON DROP · ZERO TRACE · ONE TAP SHARE*</sub>

</div>
