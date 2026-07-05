<div align="center">

# 🔗 V Share

### Le lien arrive. Aucune trace ne subsiste.

**Un outil minimaliste, sans compte et multi‑appareils pour partager du texte et des fichiers.**
Collez du texte ou glissez‑déposez un fichier, obtenez tout de suite un lien partageable et envoyez‑le à qui vous voulez — ça s'ouvre dans n'importe quel navigateur, sans rien installer.

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md)

</div>

---

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version v3.0.0](https://img.shields.io/badge/version-v3.0.0-blue.svg)](CHANGELOG.md)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-yellow.svg)](requirements.txt)
[![Langues](https://img.shields.io/badge/i18n-7%20langues-purple.svg)](#-langues--i18n)
[![Démo en ligne](https://img.shields.io/badge/demo-share.vivi.homes-ff69b4.svg)](https://share.vivi.homes)

> 🌐 Démo en ligne : **<https://share.vivi.homes>**
> 📦 Dépôt : **<https://github.com/ltdpoq-design/V-Share>**
> 📝 Notes de version : [v3.0.0 (2026‑07‑05)](https://github.com/ltdpoq-design/V-Share/releases/tag/v3.0.0)

---

## ✨ Fonctionnalités

- 🌍 **Sept langues intégrées** — English (par défaut), 简体中文, 繁體中文, 日本語, 한국어, Español, Français. Basculez d'un clic depuis le menu en haut à droite ; votre choix est conservé dans `localStorage`.
- 🔥 **Burn‑after‑read** — le lien s'autodétruit après la première ouverture : le destinataire ne le voit qu'une seule fois.
- 🎨 **Favicon néon** — un seul `favicon.svg` qui s'adapte nettement de 16 px à 256 px ; fini le flou des rasters.
- 🏷️ **Étiquette d'appareil par partage** — au moment de la création, l'appareil émetteur est enregistré pour pouvoir remonter à la source plus tard.
- 📊 **Cycle de vie explicite** — états `active` / `burned` / `expired` / `soft-deleted` ; fini les « supprimé » ambigus.
- 🔒 **Sans compte, sans pistage** — pas d'e‑mail, pas de téléphone, pas de cookies obligatoires.
- 📝 **Texte ou fichier** — notes, extraits de code, images, PDF ; plafond de **100 Mo** par fichier.
- 🔗 **Complétion automatique des liens** — collez `github.com/...` et il devient `https://github.com/...`.
- ▶️ **Améliorations YouTube** — l'URL collée devient un lecteur intégré, avec SponsorBlock pour sauter les passages sponsorisés.
- ⏱ **Expiration flexible** — choix `10 m / 30 m / 1 h / 24 h / 48 h / 72 h` ou suppression manuelle à la demande.
- 🧯 **Suppression douce de 30 jours** — les partages supprimés par erreur restent restaurables pendant un mois.
- 📡 **Approche API‑first** — chaque fonctionnalité de l'UI est aussi un endpoint REST, prêt à automatiser.

## 🚀 Démarrage rapide

Il faut **Python 3.11+**.

```bash
# 1. Cloner le dépôt
git clone https://github.com/ltdpoq-design/V-Share.git
cd V-Share

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer le serveur (par défaut sur 0.0.0.0:5001)
python3 app.py
```

Ouvrez <http://localhost:5001>, déposez un fichier ou collez du texte → cliquez sur **Share** → copiez le lien et envoyez‑le.

### Mise en production (Gunicorn)

```bash
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:5001 app:app
```

## 🌐 Langues / i18n

V Share embarque une couche de localisation complète dans `static/i18n.js` et sept tables JSON sous `static/i18n/`. Le **sélecteur de langue en haut à droite** permet de passer d'une langue à l'autre, et le choix est conservé dans le navigateur via `localStorage` (clé `vshare.lang`).

### Langues prises en charge

| Code    | Langue        |
| ------- | ------------- |
| `en`    | English       |
| `zh-CN` | 简体中文      |
| `zh-TW` | 繁體中文      |
| `ja`    | 日本語        |
| `ko`    | 한국어        |
| `es`    | Español       |
| `fr`    | Français      |

### Récupérer les tables de traduction via l'API

```bash
# Liste des langues disponibles
curl https://share.vivi.homes/api/i18n

# Table en français
curl https://share.vivi.homes/api/i18n/fr
```

## 🔌 API

| Méthode | Route                          | Description                                                  |
| ------- | ------------------------------ | ------------------------------------------------------------ |
| `POST`  | `/api/share`                   | Crée un partage de texte ou de fichier                       |
| `GET`   | `/api/share/<id>`              | Récupère un partage (compte la 1ʳᵉ ouverture si burn‑after) |
| `DELETE`| `/api/share/<id>`              | Suppression douce d'un partage                               |
| `GET`   | `/api/list`                    | Liste les partages avec leurs métadonnées                    |
| `GET`   | `/api/stats`                   | Statistiques agrégées                                        |
| `GET`   | `/api/version`                 | Version du serveur (`v3.0.0`)                               |
| `GET`   | `/api/i18n`                    | Liste des langues disponibles                                |
| `GET`   | `/api/i18n/<lang>`             | Table de traduction pour `<lang>`                            |
| `GET`   | `/s/<id>`                      | URL courte → page de visualisation                           |
| `GET`   | `/uploads/&lt;filename&gt;`    | Télécharge un fichier déjà téléversé                         |

> 🔔 Les schémas complets de requête/réponse sont documentés en commentaire dans chaque route de `app.py`.

## 🌍 Déploiement

### Exemple de reverse proxy Nginx

```nginx
server {
    listen 80;
    server_name share.example.com;

    client_max_body_size 100M;  # à aligner sur MAX_FILE_SIZE

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

En production, placez **HTTPS** (Let's Encrypt / Caddy / Cloudflare…) devant le proxy.

## 🛡 Recommandations de sécurité

- Servez toujours l'application via HTTPS en production.
- Préférez Gunicorn + systemd plutôt que le serveur de développement de Flask.
- Sauvegardez régulièrement `shares.db` : il contient tout l'historique des partages.
- Surveillez la taille de `uploads/` et prévoyez un nettoyage des fichiers expirés.
- Pour un service public, ajoutez une limitation de débit (`limit_req` Nginx ou un WAF).

## 📁 Structure du projet

```
.
├── app.py               # Backend Flask (un seul fichier)
├── index.html           # Page de création
├── view.html            # Page de lecture
├── static/
│   ├── favicon.svg      # Favicon néon (un SVG, toutes tailles)
│   ├── i18n.js          # Chargeur i18n côté client
│   └── i18n/            # Tables de traduction (en / zh-CN / zh-TW / ja / ko / es / fr)
├── uploads/             # Téléversements à l'exécution (gitignore)
├── requirements.txt
├── LICENSE
└── README.md            # ← ce fichier
```

## 📄 Licence

Distribué sous [MIT](LICENSE). Faites‑en ce que vous voulez, une attribution est toujours appréciée.

---

<div align="center">

<sub>v3.0.0 · 2026-07-05 · *NEON DROP · ZERO TRACE · ONE TAP SHARE*</sub>

</div>
