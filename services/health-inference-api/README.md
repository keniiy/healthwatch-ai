# HealthWatch AI - Inference API 🏥

Production-grade ML inference service for healthcare risk prediction.

## 📋 Overview

This service provides REST API endpoints for real-time health risk assessment based on patient metrics (age, BMI, blood pressure). Built with Clean Architecture principles, it's designed for scalability, testability, and maintainability.

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.115+
- **Python**: 3.11+
- **ML**: scikit-learn/joblib
- **Validation**: Pydantic 2.9+
- **Server**: Uvicorn (ASGI)
- **Testing**: pytest
- **Code Quality**: ruff, black, mypy
- **Deployment**: Kubernetes / Docker

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Make (for using Makefile commands)
- Docker (optional, for containerization)
- kubectl (optional, for Kubernetes deployment)

### Setup

```bash
# Complete setup (creates venv, installs deps, creates .env)
make setup

# Activate virtual environment
source venv/bin/activate

# Start development server
make dev
```

The API will be available at `http://localhost:8000`

## 📖 Makefile Commands

The project includes a comprehensive Makefile for common development tasks. Run `make help` to see all available commands.

### Setup & Installation

```bash
make setup          # Complete first-time setup
make install        # Install production dependencies
make install-dev    # Install dev dependencies
make env-setup      # Create .env from template
make venv           # Create virtual environment
```

### Development

```bash
make dev            # Run server with auto-reload (development)
make run            # Run server (production mode)
make shell          # Open Python shell with app context
make logs           # Show application logs
```

### Testing

```bash
make test           # Run all tests
make test-unit      # Run unit tests only
make test-integration  # Run integration tests only
make test-cov       # Run tests with coverage report
make test-watch     # Run tests in watch mode
```

### Code Quality

```bash
make lint           # Run linter (ruff)
make lint-fix       # Auto-fix linting issues
make format         # Format code with black
make format-check   # Check formatting without changes
make type-check     # Run type checker (mypy)
make quality        # Run all quality checks
make check          # Run tests + lint + type check
```

### Docker

```bash
make docker-build   # Build Docker image
make docker-run     # Run container (detached)
make docker-run-it  # Run container (interactive)
make docker-stop    # Stop and remove container
make docker-logs    # Show container logs
make docker-shell   # Open shell in container
make docker-clean   # Remove Docker images
```

### Kubernetes

```bash
make k8s-deploy     # Deploy to Kubernetes
make k8s-delete     # Delete from Kubernetes
make k8s-status     # Show deployment status
make k8s-logs       # Show pod logs
make k8s-shell      # Shell into pod
make k8s-restart    # Restart deployment
```

### Cleanup

```bash
make clean          # Clean cache files
make clean-all      # Deep clean (includes venv)
```

### Utilities

```bash
make help           # Show all available commands
make info           # Show project information
make api-test       # Quick API endpoint test
make ci             # Run full CI pipeline locally
```

## 🏗️ Project Structure

```text
app/
├── api/                    # API Layer (FastAPI)
│   ├── routes/            # Endpoint definitions
│   │   ├── health.py      # Health check endpoint
│   │   └── predictions.py # ML prediction endpoint
│   ├── middleware/        # Request/response middleware
│   └── deps.py            # Dependency injection
│
├── domain/                # Domain Layer (Business Logic)
│   ├── models/           # Domain entities
│   │   └── prediction.py # HealthMetrics, RiskAssessment
│   └── services/         # Business services
│       └── risk_scorer.py # Risk calculation algorithm
│
├── infrastructure/        # Infrastructure Layer
│   └── ml/
│       └── model_loader.py # ML model management
│
├── schemas/              # API Schemas (Pydantic DTOs)
│   └── prediction.py     # Request/response models
│
├── core/                 # Core utilities
│   ├── config.py        # Configuration management
│   ├── exceptions.py    # Custom exceptions
│   └── logging.py       # Structured logging
│
└── main.py              # Application entry point
```

## 🔌 API Endpoints

### Health Check

```bash
GET /api/v1/health
```

Response:

```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2025-10-10T12:00:00Z"
}
```

### Risk Prediction

```bash
POST /api/v1/predict
Content-Type: application/json

{
  "age": 45,
  "bmi": 28.5,
  "blood_pressure_systolic": 135
}
```

Response:

```json
{
  "risk_score": 0.567,
  "risk_level": "MEDIUM",
  "confidence": 0.85,
  "contributing_factors": [
    "Age (45 years) is a significant risk factor",
    "BMI (28.5) indicates overweight",
    "Blood pressure (135 mmHg) is elevated"
  ]
}
```

### Interactive Documentation

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>

## 🧪 Testing

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
pytest tests/unit/test_risk_scorer.py -v

# Run with verbose output
pytest -vv
```

### Test Structure

```text
tests/
├── unit/              # Unit tests (domain logic)
│   ├── test_risk_scorer.py
│   └── test_models.py
│
└── integration/       # Integration tests (API endpoints)
    ├── test_health.py
    └── test_predictions.py
```

## 🔧 Configuration

Configuration is managed via environment variables. Copy `.env.example` to `.env` and customize:

```bash
# Application
APP_NAME="HealthWatch AI - Inference API"
APP_VERSION="0.1.0"
DEBUG=false

# API
API_PREFIX="/api/v1"

# ML Model
MODEL_PATH="/models"
MODEL_NAME="health_risk_model.pkl"

# Logging
LOG_LEVEL="INFO"

# Server
HOST="0.0.0.0"
PORT=8000
```

## 🐳 Docker Deployment

### Build and Run

```bash
# Build image
make docker-build

# Run container
make docker-run

# Check logs
make docker-logs

# Stop container
make docker-stop
```

### Manual Docker Commands

```bash
# Build
docker build -t healthwatch-api:latest .

# Run
docker run -d -p 8000:8000 \
  -v $(pwd)/models:/models \
  --env-file .env \
  healthwatch-api:latest
```

## ☸️ Kubernetes Deployment

### Deploy to Cluster

```bash
# Deploy
make k8s-deploy

# Check status
make k8s-status

# View logs
make k8s-logs

# Shell into pod
make k8s-shell
```

### Kubernetes Resources

The `k8s/` directory contains:

- Deployment manifest
- Service definition
- ConfigMap for configuration
- PersistentVolumeClaim for model storage

## 📊 Development Workflow

### Daily Development

```bash
# 1. Start development server
make dev

# 2. Make changes to code
# (server auto-reloads)

# 3. Run tests
make test

# 4. Check code quality
make quality
```

### Before Committing

```bash
# Run full check suite
make check

# This runs:
# - All tests
# - Linting
# - Type checking
# - Format checking
```

### CI/CD Simulation

```bash
# Run the full CI pipeline locally
make ci

# This performs:
# - Clean environment
# - Install dependencies
# - Run all checks
# - Generate reports
```

## 🎯 Architecture Principles

This service follows **Clean Architecture** with clear separation of concerns:

1. **API Layer** (`app/api/`): HTTP interface, request/response handling
2. **Domain Layer** (`app/domain/`): Business logic, framework-agnostic
3. **Infrastructure Layer** (`app/infrastructure/`): External integrations (ML models, databases)
4. **Core Layer** (`app/core/`): Cross-cutting concerns (config, logging, exceptions)

### Key Benefits

- **Testability**: Business logic is independent of frameworks
- **Maintainability**: Clear separation of concerns
- **Flexibility**: Easy to swap implementations
- **Scalability**: Stateless design, ready for horizontal scaling

## 🔍 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError`

```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate
make install-dev
```

**Issue**: Port 8000 already in use

```bash
# Solution: Change port in .env or kill process
lsof -ti:8000 | xargs kill -9
# Or run on different port
PORT=8001 make dev
```

**Issue**: Tests failing

```bash
# Solution: Check test dependencies
make install-dev
make clean
make test
```

## 📚 Additional Resources

- [Main Project README](../../README.md)
- [API Documentation](http://localhost:8000/docs)
- [Architecture Decision Records](../../docs/adr/)
- [Deployment Guide](../../docs/deployment.md)

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Run `make check` to ensure quality
4. Submit a pull request

### Code Standards

- Follow PEP 8
- Write docstrings
- Add tests for new features
- Maintain >80% coverage
- Use type hints

## 📝 License

This project is part of HealthWatch AI. See [LICENSE](../../LICENSE) for details.

## 👨‍💻 Support

For issues or questions:

- Check [Troubleshooting](#-troubleshooting)
- Review [Main README](../../README.md)
- Open an issue on GitHub

---

**Built with ❤️ for better healthcare through AI
