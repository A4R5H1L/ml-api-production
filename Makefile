# Makefile for ML API Project
# Professional development workflow automation

.PHONY: help install install-dev test lint format clean docker-build docker-run docker-test

help:
	@echo "ML API - Development Commands"
	@echo "=============================="
	@echo "install        - Install production dependencies"
	@echo "install-dev    - Install development dependencies"
	@echo "test           - Run tests with coverage"
	@echo "lint           - Run linting checks"
	@echo "format         - Auto-format code"
	@echo "clean          - Clean up cache and build files"
	@echo "docker-build   - Build Docker image"
	@echo "docker-run     - Run Docker container"
	@echo "docker-test    - Test Docker container"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt
	pip install black isort flake8

test:
	pytest --cov=app --cov-report=term-missing --cov-report=html -v

lint:
	flake8 app tests --max-line-length=127
	black --check app tests
	isort --check-only app tests

format:
	black app tests
	isort app tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

docker-build:
	docker build -t ml-api:latest .

docker-run:
	docker run -p 8000:8000 --env MODEL_DEVICE=cpu ml-api:latest

docker-test:
	docker build -t ml-api:test .
	docker run --rm ml-api:test python -c "from app.main import app; print('✓ App loaded')"
	@echo "✓ Docker image test passed"
