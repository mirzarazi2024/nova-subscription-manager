# Contributing

## Local development

```bash
make setup-panels
make up
```

## Backend checks

```bash
cd backend
poetry install
poetry run ruff check app tests
poetry run black --check app tests
poetry run mypy app
poetry run pytest -q
```

## Frontend checks

```bash
cd frontend
npm install
npm run build
```

## Git policy
- Keep commits small and meaningful.
- Never commit secrets or generated caches.
- All panel integrations must support configurable API headers and endpoints.
