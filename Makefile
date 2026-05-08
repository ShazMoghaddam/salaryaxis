# =============================================================================
# SalaryAxis — Makefile
# Convenience commands for development, testing, and deployment.
#
# Usage: make <target>
# =============================================================================

.PHONY: help install test test-backend test-frontend \
        dev dev-api dev-ui \
        build build-frontend build-docker \
        run run-prod \
        deploy-aws deploy-gcp \
        clean lint

# Detect OS for open command
OPEN := $(shell command -v xdg-open 2>/dev/null || echo open)

# ─────────────────────────────────────────────────────────────────────────────
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ── Setup ─────────────────────────────────────────────────────────────────────
install: ## Install all Python and Node dependencies
	pip3 install -r requirements.txt
	cd frontend && npm install
	@echo "✓ All dependencies installed"

# ── Testing ───────────────────────────────────────────────────────────────────
test: test-backend ## Run all tests (alias for test-backend)

test-backend: ## Run Python test suite (all 3 phases, 97 tests)
	python3 -m pytest tests/ -v --tb=short

test-watch: ## Run tests in watch mode (re-runs on file change)
	python3 -m pytest tests/ -v --tb=short -f

# ── Development ───────────────────────────────────────────────────────────────
dev: ## Start both API and React dev server (requires 2 terminals)
	@echo "Start in two terminals:"
	@echo "  Terminal 1: make dev-api"
	@echo "  Terminal 2: make dev-ui"

dev-api: ## Start Flask API with hot reload on :8080
	FLASK_ENV=development LOG_LEVEL=DEBUG python3 wsgi.py

dev-ui: ## Start React Vite dev server on :3000 (proxies /api → :8080)
	cd frontend && npx vite --port 3000

dev-docker: ## Start API in Docker with hot reload (frontend via make dev-ui)
	docker compose up

# ── Build ─────────────────────────────────────────────────────────────────────
build-frontend: ## Build React SPA into static/ (for Flask to serve)
	cd frontend && npm run build
	@echo "✓ Frontend built → static/"

build: build-frontend ## Build frontend then run tests
	python3 -m pytest tests/ -q --tb=short
	@echo "✓ Full build complete"

build-docker: build-frontend ## Build the full Docker image
	docker build -t salaryaxis:latest .
	@echo "✓ Docker image built: salaryaxis:latest"

# ── Running ───────────────────────────────────────────────────────────────────
run: build-frontend ## Build frontend and start Flask (single process, dev)
	python3 wsgi.py

run-prod: build-docker ## Run the production Docker stack (nginx + api)
	docker compose -f docker-compose.prod.yml up -d
	@echo "✓ Production stack running on http://localhost"

run-docker: ## Start API in Docker (dev mode, no frontend build)
	docker compose up --build

stop: ## Stop Docker Compose stack
	docker compose down 2>/dev/null || true
	docker compose -f docker-compose.prod.yml down 2>/dev/null || true

# ── Pipeline ──────────────────────────────────────────────────────────────────
pipeline: ## Run the Phase 1 data pipeline (fetches ONS data, writes CSVs)
	python3 main.py

pipeline-refresh: ## Force-refresh all pipeline CSVs (re-fetches from NOMIS)
	FORCE_PIPELINE_REFRESH=true python3 main.py

# ── Deployment ────────────────────────────────────────────────────────────────
deploy-aws: ## Deploy to AWS ECS (requires AWS CLI + env vars)
	@[ -f .env ] && source .env; \
	chmod +x deploy/aws/deploy.sh && \
	./deploy/aws/deploy.sh $(shell git rev-parse --short HEAD)

deploy-gcp: ## Deploy to GCP Cloud Run (requires gcloud CLI + env vars)
	@[ -f .env ] && source .env; \
	chmod +x deploy/gcp/deploy.sh && \
	./deploy/gcp/deploy.sh $(shell git rev-parse --short HEAD)

setup-aws: ## One-time AWS infrastructure setup (ECR, ECS, IAM)
	chmod +x deploy/setup/aws-setup.sh && ./deploy/setup/aws-setup.sh

setup-gcp: ## One-time GCP infrastructure setup (Artifact Registry, Cloud Run)
	chmod +x deploy/setup/gcp-setup.sh && ./deploy/setup/gcp-setup.sh

# ── Cleanup ───────────────────────────────────────────────────────────────────
clean: ## Remove generated files (static/, output/, __pycache__)
	rm -rf static/ output/ frontend/dist/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✓ Cleaned"

clean-cache: ## Remove ONS API disk cache (forces re-fetch on next run)
	rm -rf output/.cache/
	@echo "✓ Cache cleared"

# ── Linting ───────────────────────────────────────────────────────────────────
lint: ## Lint Python (flake8) and JS (eslint)
	flake8 . --max-line-length 100 --exclude frontend/,output/,static/ || true
	cd frontend && npm run lint 2>/dev/null || true

# ── Utilities ─────────────────────────────────────────────────────────────────
health: ## Check the API health endpoint
	curl -s http://localhost:8080/api/v1/health | python3 -m json.tool

open: ## Open the app in your browser
	$(OPEN) http://localhost:3000 2>/dev/null || $(OPEN) http://localhost:8080

logs: ## Tail Docker Compose logs
	docker compose logs -f
