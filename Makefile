.PHONY: help install activate test lint format clean dev up down

help:
	@echo "Available targets:"
	@echo "  install      Create and activate virtual environment, install dependencies"
	@echo "  activate     Activate virtual environment (run: source venv/bin/activate)"
	@echo "  deactivate   Deactivate virtual environment (run: deactivate)"
	@echo "  dev          Run app in development mode"
	@echo "  up           Start full environment with Docker Compose"
	@echo "  down         Stop Docker Compose environment"
	@echo "  test         Run test suite"
	@echo "  lint         Run code quality checks (flake8, mypy)"
	@echo "  format       Auto-format code (black, isort)"
	@echo "  clean        Remove venv, cache, and build artifacts"
	@echo "  requirements Freeze current dependencies to requirements.txt"

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

down:
	docker-compose down

test:
	./venv/bin/python -m pytest app/tests -v

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
