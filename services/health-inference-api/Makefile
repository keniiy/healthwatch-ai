.PHONY: help install test lint format docker kind-load deploy clean logs shell

# Variables
SERVICE_NAME := health-inference-api
IMAGE_NAME := healthwatch/$(SERVICE_NAME)
IMAGE_TAG := $(shell git rev-parse --short HEAD)
K8S_NAMESPACE := healthwatch
KIND_CLUSTER := ml-platform

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(GREEN)Available commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Install dependencies with Poetry
	@echo "$(GREEN)Installing dependencies...$(NC)"
	poetry install
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

test: ## Run tests with coverage
	@echo "$(GREEN)Running tests...$(NC)"
	poetry run pytest -v --cov=app --cov-report=term-missing
	@echo "$(GREEN)✓ Tests passed$(NC)"

test-watch: ## Run tests in watch mode
	poetry run pytest-watch

lint: ## Run linters (ruff, mypy)
	@echo "$(GREEN)Running linters...$(NC)"
	poetry run ruff check app/
	poetry run mypy app/
	@echo "$(GREEN)✓ Linting passed$(NC)"

format: ## Format code with black and ruff
	@echo "$(GREEN)Formatting code...$(NC)"
	poetry run black app/ tests/
	poetry run ruff check --fix app/ tests/
	@echo "$(GREEN)✓ Code formatted$(NC)"

format-check: ## Check code formatting without modifying
	poetry run black --check app/ tests/
	poetry run ruff check app/ tests/

run: ## Run development server
	@echo "$(GREEN)Starting development server...$(NC)"
	poetry run uvicorn app.main:app --reload --port 8000

shell: ## Open Poetry shell
	poetry shell

docker-build: ## Build Docker image
	@echo "$(GREEN)Building Docker image...$(NC)"
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(IMAGE_NAME):latest
	@echo "$(GREEN)✓ Image built: $(IMAGE_NAME):$(IMAGE_TAG)$(NC)"

docker-run: ## Run Docker container locally
	@echo "$(GREEN)Running Docker container...$(NC)"
	docker run -p 8000:8000 \
		--env-file .env \
		$(IMAGE_NAME):latest

kind-load: docker-build ## Load Docker image into Kind cluster
	@echo "$(GREEN)Loading image into Kind cluster...$(NC)"
	kind load docker-image $(IMAGE_NAME):$(IMAGE_TAG) --name $(KIND_CLUSTER)
	kind load docker-image $(IMAGE_NAME):latest --name $(KIND_CLUSTER)
	@echo "$(GREEN)✓ Image loaded into Kind$(NC)"

k8s-apply: ## Apply Kubernetes manifests
	@echo "$(GREEN)Applying Kubernetes manifests...$(NC)"
	kubectl apply -f k8s/
	@echo "$(GREEN)✓ Manifests applied$(NC)"

k8s-delete: ## Delete Kubernetes resources
	kubectl delete -f k8s/

deploy: kind-load k8s-apply ## Full deployment (build, load, apply)
	@echo "$(GREEN)Waiting for deployment...$(NC)"
	kubectl rollout status deployment/$(SERVICE_NAME) -n $(K8S_NAMESPACE)
	@echo "$(GREEN)✓ Deployment complete!$(NC)"
	@echo "$(YELLOW)Service available at: http://localhost:30000$(NC)"

logs: ## Show pod logs (follow)
	kubectl logs -f -l app=$(SERVICE_NAME) -n $(K8S_NAMESPACE)

describe: ## Describe the deployment
	kubectl describe deployment $(SERVICE_NAME) -n $(K8S_NAMESPACE)

pods: ## List pods
	kubectl get pods -n $(K8S_NAMESPACE) -l app=$(SERVICE_NAME)

port-forward: ## Port forward to pod (8000 -> 8000)
	kubectl port-forward -n $(K8S_NAMESPACE) \
		svc/$(SERVICE_NAME) 8000:8000

exec: ## Execute shell in pod
	kubectl exec -it -n $(K8S_NAMESPACE) \
		$$(kubectl get pod -n $(K8S_NAMESPACE) -l app=$(SERVICE_NAME) -o jsonpath='{.items[0].metadata.name}') \
		-- /bin/bash

clean: ## Clean up build artifacts
	@echo "$(GREEN)Cleaning up...$(NC)"
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov dist build *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✓ Cleaned$(NC)"

setup: install ## Initial setup (install + create .env)
	@if [ ! -f .env ]; then \
		echo "$(YELLOW)Creating .env file...$(NC)"; \
		cp .env.example .env; \
		echo "$(GREEN)✓ .env created. Please edit with your values.$(NC)"; \
	else \
		echo "$(YELLOW).env already exists$(NC)"; \
	fi

ci: format-check lint test ## Run CI checks (format, lint, test)
	@echo "$(GREEN)✓ All CI checks passed!$(NC)"

.DEFAULT_GOAL := help
