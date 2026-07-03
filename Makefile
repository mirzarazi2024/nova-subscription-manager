.PHONY: up down backend frontend test lint

up:
	docker compose up --build

down:
	docker compose down -v

backend:
	cd backend && poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend:
	cd frontend && npm run dev

test:
	cd backend && poetry run pytest -q

lint:
	cd backend && poetry run ruff check app tests && poetry run black --check app tests && poetry run mypy app

setup-panels:
	python3 infra/scripts/setup_panels.py
