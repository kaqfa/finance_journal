.PHONY: install dev build test clean docker-up docker-down

# Install all dependencies
install:
	npm install
	cd apps/backend && pip install -r requirements.txt

# Start development servers
dev:
	npm run dev

# Start development with Docker
docker-dev:
	docker-compose up --build

# Build applications
build:
	npm run build

# Run tests
test:
	npm run test

# Clean build artifacts
clean:
	npm run clean
	cd apps/frontend && rm -rf .next out
	cd apps/backend && find . -name "*.pyc" -delete && find . -name "__pycache__" -delete

# Setup environment
setup: install
	cd apps/backend && python manage.py migrate
	cd apps/backend && python manage.py collectstatic --noinput

# Docker commands
docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Lint and format
lint:
	npm run lint

format:
	npm run format

# Database operations
migrate:
	cd apps/backend && python manage.py migrate

makemigrations:
	cd apps/backend && python manage.py makemigrations

# Help
help:
	@echo "Available commands:"
	@echo "  install       - Install all dependencies"
	@echo "  dev          - Start development servers"
	@echo "  docker-dev   - Start development with Docker"
	@echo "  build        - Build applications"
	@echo "  test         - Run tests"
	@echo "  clean        - Clean build artifacts"
	@echo "  setup        - Setup environment"
	@echo "  docker-up    - Start Docker containers"
	@echo "  docker-down  - Stop Docker containers"
	@echo "  lint         - Run linting"
	@echo "  format       - Format code"
	@echo "  migrate      - Run Django migrations"