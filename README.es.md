<div align="center">

# 🔗 V Share

### El enlace llega. No quedan huellas.

**Una herramienta minimalista, sin cuentas y multiplataforma para compartir texto y archivos.**
Pega texto o arrastra un archivo, obtén al instante un enlace compartible y mándaselo a quien quieras — se abre en cualquier navegador, sin instalar nada.

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md)

</div>

---

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Versión v3.0.0](https://img.shields.io/badge/versi%C3%B3n-v3.0.0-blue.svg)](CHANGELOG.md)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-yellow.svg)](requirements.txt)
[![Idiomas](https://img.shields.io/badge/i18n-7%20idiomas-purple.svg)](#-idiomas--i18n)

> 📦 Repositorio: **<https://github.com/ltdpoq-design/V-Share>**
> 📝 Notas de la versión: [v3.0.0 (2026-07-05)](https://github.com/ltdpoq-design/V-Share/releases/tag/v3.0.0)

---

## ✨ Características

- 🌍 **Siete idiomas de fábrica** — English (predeterminado), 简体中文, 繁體中文, 日本語, 한국어, Español, Français. Cambia con un clic desde el menú superior derecho; tu preferencia queda en `localStorage`.
- 🔥 **Burn-after-read** — el enlace se autodestruye tras la primera apertura, así el destinatario solo lo ve una vez.
- 🎨 **Favicon neón** — un único `favicon.svg` se escala perfectamente de 16 px a 256 px; se acabó el blur de los PNGs.
- 🏷️ **Etiqueta de dispositivo por compartida** — al crear el enlace se registra el dispositivo de origen para que luego puedas rastrear de dónde salió.
- 📊 **Ciclo de vida explícito** — estados `active` / `burned` / `expired` / `soft-deleted`. Nada de “borrado” ambiguo.
- 🔒 **Sin cuentas, sin rastreo** — sin correo, sin teléfono, sin cookies obligatorias.
- 📝 **Texto o archivo** — notas, snippets de código, imágenes, PDF; tope de **100 MB** por archivo.
- 🔗 **Autocompletado de enlaces** — pegas `github.com/...` y se convierte en `https://github.com/...`.
- ▶️ **Mejoras para YouTube** — la URL pegada se vuelve un reproductor embebido, con SponsorBlock para saltar patrocinios.
- ⏱ **Caducidad flexible** — opciones `10 m / 30 m / 1 h / 24 h / 48 h / 72 h` o borrado manual al instante.
- 🧯 **Borrado suave durante 30 días** — los enlaces borrados por accidente se pueden recuperar durante un mes.
- 📡 **Diseño API-first** — todo lo que ves en la UI también es un endpoint REST, listo para automatizar.

## 🚀 Inicio rápido

Necesitas **Python 3.11+**.

```bash
# 1. Clona el repo
git clone https://github.com/ltdpoq-design/V-Share.git
cd V-Share

# 2. Instala dependencias
pip install -r requirements.txt

# 3. Arranca el servidor (por defecto, 0.0.0.0:5001)
python3 app.py
```

Abre <http://localhost:5001>, suelta un archivo o pega texto → pulsa **Share** → copia el enlace y mándalo.

### Producción (Gunicorn)

```bash
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:5001 app:app
```

## 🌐 Idiomas / i18n

V Share incluye una capa de localización completa en `static/i18n.js` y siete tablas JSON bajo `static/i18n/`. El **selector de idioma de la esquina superior derecha** permite cambiar entre los siete idiomas disponibles, y la elección se guarda en el navegador con `localStorage` (clave `vshare.lang`).

### Locales disponibles

| Código   | Idioma        |
| -------- | ------------- |
| `en`     | English       |
| `zh-CN`  | 简体中文      |
| `zh-TW`  | 繁體中文      |
| `ja`     | 日本語        |
| `ko`     | 한국어        |
| `es`     | Español       |
| `fr`     | Français      |

### Obtener tablas de traducción por API

```bash
# Lista de idiomas disponibles
curl http://127.0.0.1:5001/api/i18n

# Tabla en español
curl http://127.0.0.1:5001/api/i18n/es
```

## 🔌 API

| Método   | Ruta                          | Descripción                                          |
| -------- | ----------------------------- | ---------------------------------------------------- |
| `POST`   | `/api/share`                  | Crea un compartido de texto o archivo                |
| `GET`    | `/api/share/<id>`             | Recupera un compartido (cuenta la primera apertura)   |
| `DELETE` | `/api/share/<id>`             | Borrado suave de un compartido                       |
| `GET`    | `/api/list`                   | Lista los compartidos con sus metadatos              |
| `GET`    | `/api/stats`                  | Estadísticas agregadas                              |
| `GET`    | `/api/version`                | Versión del servidor (`v3.0.0`)                      |
| `GET`    | `/api/i18n`                   | Lista de idiomas disponibles                        |
| `GET`    | `/api/i18n/<lang>`            | Tabla de traducción de un idioma                    |
| `GET`    | `/s/<id>`                     | URL corta → página de visualización                  |
| `GET`    | `/uploads/&lt;filename&gt;`   | Descarga un archivo subido                           |

> 🔔 Los esquemas completos de petición/respuesta están en los comentarios de cada ruta en `app.py`.

## 🌍 Despliegue

### Nginx como reverse proxy

```nginx
server {
    listen 80;
    server_name share.example.com;

    client_max_body_size 100M;  # igual que MAX_FILE_SIZE

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

En producción, pon **HTTPS** (Let's Encrypt / Caddy / Cloudflare…) delante del proxy.

## 🛡 Notas de seguridad

- Atento: en producción, sirve siempre bajo HTTPS.
- Prefiere Gunicorn + systemd en lugar del servidor de desarrollo de Flask.
- Haz copia de seguridad de `shares.db` regularmente: contiene todo el historial.
- Vigila el tamaño de `uploads/` y añade un script que retire los archivos caducados.
- Si es público, añade rate limiting (por ejemplo, `limit_req` de Nginx o un WAF).

## 📁 Estructura del proyecto

```
.
├── app.py               # Backend Flask (un solo archivo)
├── index.html           # Página para crear compartidos
├── view.html            # Página para recibirlos
├── static/
│   ├── favicon.svg      # Favicon neón (un SVG, todos los tamaños)
│   ├── i18n.js          # Cargador de i18n del cliente
│   └── i18n/            # Tablas de traducción (en / zh-CN / zh-TW / ja / ko / es / fr)
├── uploads/             # Subidas en ejecución (ignorado por git)
├── requirements.txt
├── LICENSE
└── README.md            # ← este fichero
```

## 📄 Licencia

Distribuido bajo [MIT](LICENSE). Úsalo libremente, una atribución se agradece.

---

<div align="center">

<sub>v3.0.0 · 2026-07-05 · *NEON DROP · ZERO TRACE · ONE TAP SHARE*</sub>

</div>
