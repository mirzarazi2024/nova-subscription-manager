# NSM Server Installation Guide

This guide installs NOVA Subscription Manager (NSM) on a server separate from your Hiddify server.

## 1) Requirements

Recommended server:
- Ubuntu 22.04/24.04
- 2 CPU / 2 GB RAM minimum for testing
- Public IP or private network route to Hiddify
- Open ports: `80`, optionally `9090`, `3001` for monitoring tests

Install base packages:

```bash
sudo apt update
sudo apt install -y git curl ca-certificates nano
```

Install Docker:

```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
newgrp docker
```

Verify:

```bash
docker --version
docker compose version
```

---

## 2) Clone repository

```bash
git clone https://github.com/mirzarazi2024/nova-subscription-manager.git
cd nova-subscription-manager
```

---

## 3) Configure environment

```bash
cp backend/.env.example backend/.env
nano backend/.env
```

Minimum recommended values:

```env
APP_ENV=production
SECRET_KEY=replace-with-a-long-random-secret
POSTGRES_DSN=postgresql+asyncpg://nsm:nsm@postgres:5432/nsm
REDIS_DSN=redis://redis:6379/0
PANEL_CONFIG_PATH=config/panels.json
CORS_ORIGINS=["http://YOUR_SERVER_IP"]
```

Generate a random secret if needed:

```bash
openssl rand -hex 32
```

---

## 4) Configure Hiddify API

Run:

```bash
make setup-panels
```

For Hiddify, use:

| Field | Value |
|---|---|
| Panel type | `hiddify` |
| Base URL | `https://YOUR_HIDDIFY_DOMAIN` |
| API Key | Hiddify Admin API Key |
| API Header Name | `Hiddify-API-Key` |
| API Prefix | empty |
| Proxy Path | **Proxy Path for Admins** |
| Test Endpoint | `/api/v2/admin/user/` |

### Which Hiddify Proxy Path should I use?

Hiddify has two different proxy paths:

1. **Proxy Path for Admins**
   - Use this in NSM API configuration.
   - It is used for Admin API routes like:
     - `/{proxy_path}/api/v2/admin/user/`
     - `/{proxy_path}/api/v2/admin/me/`
     - `/{proxy_path}/api/v2/panel/info/`

2. **Proxy Path for Clients**
   - Do **not** use this for NSM admin API connection.
   - It is for client/subscription access routes and hiding client-facing proxy/sub links.

So in NSM `proxy_path`, enter **Proxy Path for Admins**.

If your Admin Proxy Path is `admin-secret`, NSM will call:

```text
https://YOUR_HIDDIFY_DOMAIN/admin-secret/api/v2/admin/user/
```

If Hiddify API works without a proxy path, leave it empty and NSM will call:

```text
https://YOUR_HIDDIFY_DOMAIN/api/v2/admin/user/
```

---

## 5) Test Hiddify access from NSM server

With Admin proxy path:

```bash
curl -i \
  -H "Hiddify-API-Key: YOUR_HIDDIFY_API_KEY" \
  "https://YOUR_HIDDIFY_DOMAIN/YOUR_ADMIN_PROXY_PATH/api/v2/admin/user/"
```

Important: do **not** use the Swagger/docs URL for API calls. This is wrong:

```text
https://YOUR_HIDDIFY_DOMAIN/YOUR_ADMIN_PROXY_PATH/api/docs#/paths/...
```

Use the real REST endpoint only:

```text
https://YOUR_HIDDIFY_DOMAIN/YOUR_ADMIN_PROXY_PATH/api/v2/admin/user/
```

Without proxy path:

```bash
curl -i \
  -H "Hiddify-API-Key: YOUR_HIDDIFY_API_KEY" \
  "https://YOUR_HIDDIFY_DOMAIN/api/v2/admin/user/"
```

Expected result:
- `200`: OK
- `401/403`: API key or permission problem
- timeout/connect error: firewall/network/SSL problem

---

## 6) Start NSM

```bash
docker compose up --build -d
```

Check containers:

```bash
docker compose ps
```

Check logs:

```bash
docker compose logs -f backend
```

---

## 7) Open services

| Service | URL |
|---|---|
| Dashboard | `http://YOUR_SERVER_IP` |
| API Docs | `http://YOUR_SERVER_IP/api/docs` |
| Health | `http://YOUR_SERVER_IP/health` |
| Metrics | `http://YOUR_SERVER_IP/metrics` |
| Prometheus | `http://YOUR_SERVER_IP:9090` |
| Grafana | `http://YOUR_SERVER_IP:3001` |

Grafana default:

```text
admin / admin
```

---

## 8) Get NSM admin token for API testing

```bash
curl -X POST http://YOUR_SERVER_IP/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
```

Use returned `access_token`:

```bash
curl http://YOUR_SERVER_IP/api/v1/panels \
  -H "Authorization: Bearer YOUR_NSM_TOKEN"
```

---

## 9) Test Auto Detect from NSM API

```bash
curl -X POST http://YOUR_SERVER_IP/api/v1/panels/auto-detect \
  -H "Authorization: Bearer YOUR_NSM_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "panel_type": "hiddify",
    "base_url": "https://YOUR_HIDDIFY_DOMAIN",
    "api_key": "YOUR_HIDDIFY_API_KEY",
    "verify_ssl": true,
    "proxy_path": "YOUR_ADMIN_PROXY_PATH"
  }'
```

---

## 10) Update later

```bash
git pull
docker compose up --build -d
```

---

## Troubleshooting

### API returns 404
Usually wrong proxy path. Use **Proxy Path for Admins**, not clients.

### API returns 401/403
Wrong API key or insufficient admin permission.

### curl timeout
Network/firewall/DNS/SSL issue between NSM server and Hiddify server.

### Dashboard opens but API fails
Check Nginx/backend logs:

```bash
docker compose logs -f nginx
docker compose logs -f backend
```

If `docker compose ps` does not show a running `backend` container, the Dashboard cannot save/test anything. Fix backend first, then reload the Dashboard.
