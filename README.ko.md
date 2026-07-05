<div align="center">

# 🔗 V Share

### 링크는 도착하고, 흔적은 남기지 않는다.

**미니멀하고 무가입, 기기를 가리지 않는 텍스트·파일 공유 도구입니다.**
텍스트를 붙여넣거나 파일을 끌어다 놓으면 즉시 공유 링크가 생성됩니다. 받는 쪽은 브라우저만 있으면 되고, 클라이언트 설치는 필요 없습니다.

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md)

</div>

---

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![버전 v3.0.0](https://img.shields.io/badge/%EB%B2%84%EC%A0%84-v3.0.0-blue.svg)](CHANGELOG.md)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-yellow.svg)](requirements.txt)
[![다국어](https://img.shields.io/badge/i18n-7%EA%B0%9C%EC%96%B8%EC%96%B4-purple.svg)](#-다국어--i18n)
[![라이브 데모](https://img.shields.io/badge/demo-share.vivi.homes-ff69b4.svg)](https://share.vivi.homes)

> 🌐 라이브 데모：**<https://share.vivi.homes>**
> 📦 저장소：**<https://github.com/ltdpoq-design/V-Share>**
> 📝 릴리스 노트：[v3.0.0 (2026-07-05)](https://github.com/ltdpoq-design/V-Share/releases/tag/v3.0.0)

---

## ✨ 주요 기능

- 🌍 **7개 언어 기본 제공** — English(기본), 简体中文, 繁體中文, 日本語, 한국어, Español, Français. 우측 상단 메뉴에서 한 번에 전환할 수 있으며, 선택은 `localStorage`에 저장됩니다.
- 🔥 **열람 후 자동 소각(burn-after-read)** — 링크를 한 번 열면 즉시 사라져, 받는 사람은 딱 한 번만 볼 수 있습니다.
- 🎨 **네온 파비콘** — 단일 `favicon.svg`가 16 px부터 256 px까지 알아서 선명하게 그려집니다. 더는 흐릿하지 않습니다.
- 🏷️ **공유별 기기 태그** — 생성 시 발신 기기 이름을 함께 기록해 두어, 나중에 출처를 추적할 수 있습니다.
- 📊 **명확한 공유 수명 주기** — `active` / `burned` / `expired` / `soft-deleted` 상태를 명확히 구분해, 모호한 “삭제” 플래그를 정리했습니다.
- 🔒 **무가입, 무추적** — 이메일, 전화번호, 쿠키까지 일절 요구하지 않습니다.
- 📝 **텍스트와 파일 모두 지원** — 짧은 글, 코드 스니펫, 이미지, PDF. 파일당 최대 **100 MB**.
- 🔗 **링크 자동 완성** — `github.com/...`처럼 붙여넣으면 자동으로 `https://github.com/...`로 만들어 줍니다.
- ▶️ **YouTube 확장** — 붙여넣은 URL을 임베드 플레이어로 자동 펼치고, SponsorBlock로 광고·협찬 구간을 건너뜁니다.
- ⏱ **유연한 만료 시간** — `10분 / 30분 / 1시간 / 24시간 / 48시간 / 72시간` 옵션과 수동 삭제를 함께 제공합니다.
- 🧯 **30일 소프트 삭제 보존** — 실수로 지워도 30일 안이면 복구할 수 있고, 만료 시 자동으로 비워집니다.
- 📡 **API 우선 설계** — 모든 UI 기능은 REST API로도 제공되어, 스크립트 연동이 간편합니다.

## 🚀 빠른 시작

**Python 3.11 이상**이 필요합니다.

```bash
# 1. 저장소 복제
git clone https://github.com/ltdpoq-design/V-Share.git
cd V-Share

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 서버 실행 (기본: 0.0.0.0:5001)
python3 app.py
```

브라우저에서 <http://localhost:5001>을 열고 파일을 드롭하거나 텍스트를 붙여넣은 뒤 → **Share** 클릭 → 링크를 복사해 상대에게 전달하세요.

### 운영 환경 (Gunicorn)

```bash
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:5001 app:app
```

## 🌐 다국어 / i18n

V Share는 `static/i18n.js`와 `static/i18n/` 안의 7개 JSON 테이블로 완전한 로컬라이제이션을 제공합니다. **우측 상단의 언어 스위처**로 7개 언어 중 하나를 고르면, 선택은 `localStorage`(키 이름 `vshare.lang`)에 보존되어 다음 방문 때도 그대로 적용됩니다.

### 지원 로케일

| 코드     | 언어         |
| -------- | ------------ |
| `en`     | English      |
| `zh-CN`  | 简体中文     |
| `zh-TW`  | 繁體中文     |
| `ja`     | 日本語       |
| `ko`     | 한국어       |
| `es`     | Español      |
| `fr`     | Français     |

### API로 번역 테이블 가져오기

```bash
# 지원 언어 목록
curl https://share.vivi.homes/api/i18n

# 한국어 번역 테이블
curl https://share.vivi.homes/api/i18n/ko
```

## 🔌 API

| 메서드    | 경로                          | 설명                                          |
| --------- | ----------------------------- | --------------------------------------------- |
| `POST`    | `/api/share`                  | 텍스트/파일 공유 생성                         |
| `GET`     | `/api/share/<id>`             | 공유 조회 (열람 후 소형은 1회로 카운트)        |
| `DELETE`  | `/api/share/<id>`             | 공유 소프트 삭제                              |
| `GET`     | `/api/list`                   | 공유와 메타데이터 목록                        |
| `GET`     | `/api/stats`                  | 집계 통계                                     |
| `GET`     | `/api/version`                | 서버 버전 (`v3.0.0`)                          |
| `GET`     | `/api/i18n`                   | 지원 언어 목록                                |
| `GET`     | `/api/i18n/<lang>`            | 지정 언어의 번역 테이블                       |
| `GET`     | `/s/<id>`                     | 단축 URL → 보기 페이지                        |
| `GET`     | `/uploads/&lt;filename&gt;`   | 업로드한 파일 다운로드                       |

> 🔔 요청/응답의 자세한 스키마는 `app.py` 각 라우트의 주석에 적혀 있습니다.

## 🌍 배포

### Nginx 리버스 프록시 예시

```nginx
server {
    listen 80;
    server_name share.example.com;

    client_max_body_size 100M;  # MAX_FILE_SIZE 와 동일하게

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

운영 환경에서는 **HTTPS**(Let's Encrypt / Caddy / Cloudflare 등)를 프록시 앞단에 반드시 두시기 바랍니다.

## 🛡 보안 가이드

- 운영에서는 반드시 HTTPS로 서비스하세요.
- Flask 개발 서버 대신 Gunicorn + systemd 조합을 권장합니다.
- `shares.db`는 모든 공유 기록을 담고 있으므로 정기적으로 백업하세요.
- `uploads/` 폴더의 크기를 모니터링하고, 만료 파일을 정리하는 잡을 추가하세요.
- 공개 운영 시에는 Nginx `limit_req` 같은 속도 제한 또는 WAF 도입을 권장합니다.

## 📁 프로젝트 구조

```
.
├── app.py               # Flask 백엔드 (단일 파일)
├── index.html           # 공유 생성 페이지
├── view.html            # 공유 열람 페이지
├── static/
│   ├── favicon.svg      # 네온 파비콘 (단일 SVG, 모든 크기 대응)
│   ├── i18n.js          # 클라이언트 i18n 로더
│   └── i18n/            # 번역 테이블 (en / zh-CN / zh-TW / ja / ko / es / fr)
├── uploads/             # 런타임 업로드 디렉터리 (.gitignore 처리됨)
├── requirements.txt
├── LICENSE
└── README.md            # ← 지금 보고 계신 파일
```

## 📄 라이선스

이 프로젝트는 [MIT](LICENSE) 라이선스를 따릅니다. 자유롭게 사용하시고, 출처를 남겨 주시면 기쁘겠습니다.

---

<div align="center">

<sub>v3.0.0 · 2026-07-05 · *NEON DROP · ZERO TRACE · ONE TAP SHARE*</sub>

</div>
