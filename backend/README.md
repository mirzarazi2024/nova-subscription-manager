# NSM Backend

Enterprise-grade backend for NOVA Subscription Manager.

## Run

```bash
poetry install
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
