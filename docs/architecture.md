# NOVA Subscription Manager – Architecture (Sprint 1)

## Principles
- Clean Architecture + DDD
- Async-first backend (FastAPI + SQLAlchemy Async)
- Pluggable parser SDK
- Horizontal scalability compatible (shared PostgreSQL + Redis)

## Backend Modules
- `api`: HTTP contracts
- `application`: use-cases and DTOs
- `domain`: core merge and fingerprint logic
- `infrastructure`: external systems (Hiddify API, scheduler)
- `plugins`: parser SDK and registry

## Implemented Enterprise Features (Initial)
- Multi-table production schema for all required entities
- JWT + RBAC baseline
- Provider manager CRUD/list/refresh API
- Smart Provider Scoring (initial weighted formula)
- Subscription Preview endpoint
- Merge engine with SHA256 fingerprint dedup
- APScheduler background jobs
- Prometheus metrics endpoint

## Frontend
- Next.js 15 dashboard shell with main enterprise pages
- Provider listing page
- Subscription preview UI

## Infra
- Dockerized backend/frontend + Nginx reverse proxy
- PostgreSQL + Redis
- Prometheus + Grafana
- CI pipeline for lint/test/build

## Next Sprint Targets
1. Real Hiddify sync pipelines (users/domains/subscriptions)
2. Full provider parsing pipeline + node persistence
3. Rule engine + health engine implementation
4. Analytics widgets and charts
5. API key management, auditing, and hardened security controls
