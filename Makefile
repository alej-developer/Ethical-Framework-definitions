# EN: Root automation Makefile for the AI Ethics Interactive Simulator | ES: Makefile de automatizacion raiz para el Simulador Interactivo de Etica en IA

.PHONY: help install lint format test build dev-backend dev-frontend all

help:
	@echo "AI Ethics Interactive Simulator - Automation Commands"
	@echo "  make install       - EN: Install backend and frontend dependencies | ES: Instalar dependencias"
	@echo "  make lint          - EN: Run static type checking and linting | ES: Ejecutar tipado estatico y linting"
	@echo "  make format        - EN: Format code with Ruff | ES: Formatear codigo con Ruff"
	@echo "  make test          - EN: Run automated unit and integration tests | ES: Ejecutar pruebas automatizadas"
	@echo "  make build         - EN: Type-check and compile frontend bundle | ES: Compilar frontend"
	@echo "  make dev-backend   - EN: Start FastAPI server with live reload | ES: Iniciar backend FastAPI"
	@echo "  make dev-frontend  - EN: Start Vite development server | ES: Iniciar servidor Vite"
	@echo "  make all           - EN: Full pipeline (install, lint, test, build) | ES: Tuberia completa"

install:
	@echo "Installing backend dependencies with Poetry..."
	cd backend && poetry install
	@echo "Installing frontend dependencies with npm..."
	cd frontend && npm install

lint:
	@echo "Running Ruff linter on backend..."
	cd backend && poetry run ruff check .
	@echo "Running strict Mypy type checker on backend..."
	cd backend && poetry run mypy domain application infrastructure tests

format:
	@echo "Formatting backend code with Ruff..."
	cd backend && poetry run ruff format .
	cd backend && poetry run ruff check --fix .

test:
	@echo "Running Pytest test suite..."
	cd backend && poetry run pytest -v

build:
	@echo "Building frontend distribution..."
	cd frontend && npm run build

dev-backend:
	@echo "Starting backend development server on port 8000..."
	cd backend && poetry run uvicorn infrastructure.main:app --reload --host 127.0.0.1 --port 8000

dev-frontend:
	@echo "Starting frontend development server on port 5173..."
	cd frontend && npm run dev

all: install lint test build
