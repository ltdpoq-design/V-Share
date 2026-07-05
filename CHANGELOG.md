# V Share Changelog

## v3.0.0 — 2026-07-05
### 🌍 Six languages
- English (default), 简体中文, 繁體中文, 日本語, 한국어, Español, Français

### 🎨 New neon favicon
- Single SVG with internal scaling (looks crisp at 16/32/64/256 px)

### 🔥 Burn-after-read
- Share can self-destruct after first view

### 🏷️ Per-share device tags
- Record the device name on share creation

### 📊 New share lifecycle states
- `active` / `burned` / `expired` / `soft-deleted`

### 🔤 `/api/i18n` and `/api/i18n/<lang>` endpoints
- Client fetch translation tables

### 🛠 DevOps
- Top-right language switcher with localStorage persistence
- Full data-i18n coverage on index.html / view.html

## v2.9.2 — 2026-06-30
- Maintenance release