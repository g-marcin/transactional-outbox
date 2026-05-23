.PHONY: help install activate test lint format clean dev up down

help:
	@echo "Available targets:"
	@echo "  install      Create and activate virtual environment, install dependencies"
	@echo "  activate     Activate virtual environment (run: source venv/bin/activate)"
	@echo "  deactivate   Deactivate virtual environment (run: deactivate)"
	@echo "  dev          Run app in development mode"
	@echo "  up           Start full environment with Docker Compose"
	@echo "  up-seed      Start environment and seed with 50 orders"
	@echo "  down         Stop Docker Compose environment"
	@echo "  test         Run test suite (isolated with testcontainers)"
	@echo "  test-docker  Run test suite against running docker-compose db"
	@echo "  seed         Create 50 orders via API (populates orders + outbox)"
	@echo "  kick-worker  Manually trigger worker to process pending outbox entries"
	@echo "  stats        Show outbox statistics (PENDING, PROCESSED, FAILED counts)"
	@echo "  pgadmin      Open pgAdmin in browser (shows credentials)"
	@echo "  lint         Run code quality checks (ruff, mypy)"
	@echo "  format       Auto-format code (ruff)"
	@echo "  clean        Remove venv, cache, and build artifacts"
	@echo "  requirements Freeze current dependencies to requirements.txt"
	@echo "  docs         Generate OpenAPI docs (JSON, HTML, Markdown)"
	@echo "  docs-json    Generate OpenAPI JSON schema"
	@echo "  docs-html    Generate standalone HTML documentation"
	@echo "  docs-markdown Generate Markdown documentation"

install:
	python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r app/requirements.txt -r app/requirements-dev.txt
	@echo "\n✓ Virtual environment created. Run: source venv/bin/activate"

activate:
	@echo "Run this command: source venv/bin/activate"

deactivate:
	@echo "Run this command: deactivate"

dev:
	./venv/bin/python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

up:
	docker-compose up

up-seed:
	SEED_DATA=true SEED_COUNT=50 docker-compose up

down:
	docker-compose down

test:
	./venv/bin/python -m pytest app/tests -v

test-docker:
	DATABASE_URL=postgresql://postgres:postgres@localhost:5432/outbox_demo ./venv/bin/python -m pytest app/tests -v

lint:
	./venv/bin/ruff check app
	./venv/bin/ruff format --check app
	./venv/bin/mypy app

format:
	./venv/bin/ruff check --fix app
	./venv/bin/ruff format app

clean:
	rm -rf venv
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache dist build *.egg-info

requirements:
	./venv/bin/pip freeze > app/requirements.txt

seed:
	./venv/bin/python scripts/seed_orders.py --count 50 --delay 0.1

kick-worker:
	./venv/bin/python scripts/outbox_kick.py

stats:
	./venv/bin/python scripts/outbox_stats.py

pgadmin:
	./venv/bin/python scripts/open_pgadmin.py

docs:
	./venv/bin/python scripts/generate_docs.py --all

docs-json:
	./venv/bin/python scripts/generate_docs.py --json

docs-html:
	./venv/bin/python scripts/generate_docs.py --html

docs-markdown:
	./venv/bin/python scripts/generate_docs.py --markdown
