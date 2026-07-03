# NOVA Subscription Manager (NSM)

Enterprise-grade subscription management platform integrating with Hiddify via REST API.

> GitHub-ready monorepo: FastAPI backend, Next.js dashboard, Docker Compose, CI, monitoring, and configurable multi-panel API profiles.

## Quick Start

```bash
make setup-panels
docker compose up --build
```

> قبل از اجرا، با `make setup-panels` API Key و URL پنل‌ها (خصوصا Hiddify) را از کاربر بگیرید.

For full server installation, see [`INSTALL.md`](INSTALL.md).

## Hiddify API Profile

For the provided Hiddify OpenAPI schema, configure:

- Header: `Hiddify-API-Key`
- Prefix: empty
- Test endpoint: `/api/v2/admin/user/`
- Optional proxy path: your panel proxy path if present
- For Hiddify, use **Proxy Path for Admins** in NSM, not **Proxy Path for Clients**.

The Dashboard `Panels` page includes **Test Connection** and **Auto Detect**.

Endpoints:
- App: http://localhost
- API docs: http://localhost/api/docs
- Health: http://localhost/health
- Metrics: http://localhost/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001

## Structure
- `backend/` FastAPI, SQLAlchemy, Alembic
- `frontend/` Next.js 15 admin dashboard
- `infra/` Nginx, Prometheus, Grafana configs
- `.github/workflows/` CI pipeline

## Panel Configuration
- Wizard: `make setup-panels`
- Output: `backend/config/panels.json`
- Docs: `docs/panel-setup.md`
- Required APIs + how to obtain tokens: `docs/hiddify-api-requirements.md`
