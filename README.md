# HealthWatch AI 🏥

A cloud-native health risk assessment platform powered by machine learning, designed to predict patient health risks based on key health metrics.

## 📋 Overview

HealthWatch AI is a production-ready ML inference system that analyzes patient health data (age, BMI, blood pressure) to generate personalized risk assessments. Built with modern software engineering practices, it demonstrates a complete ML deployment pipeline from model serving to Kubernetes orchestration.

### Key Features

- **Real-time Risk Assessment**: Instant health risk predictions based on patient metrics
- **Multi-Level Risk Classification**: Categorizes patients into LOW, MEDIUM, HIGH, and CRITICAL risk levels
- **Contributing Factor Analysis**: Identifies which health metrics drive the risk score
- **Cloud-Native Architecture**: Kubernetes-ready with containerized microservices
- **Production-Grade Design**: Clean architecture, comprehensive logging, and error handling
- **Scalable Infrastructure**: Multi-node Kubernetes cluster for ML workloads

## 🏗️ Architecture

```markdown
┌─────────────────────────────────────────────────────────┐
│                    HealthWatch AI                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Health Inference API (FastAPI)           │  │
│  │                                                   │  │
│  │  API Layer        Domain Layer    Infrastructure │  │
│  │  ├─ Routes        ├─ Models       ├─ ML Models  │  │
│  │  ├─ Middleware    ├─ Services     └─ Config     │  │
│  │  └─ Schemas       └─ Business Logic              │  │
│  └──────────────────────────────────────────────────┘  │
│                         ↕                                │
│  ┌──────────────────────────────────────────────────┐  │
│  │     Kubernetes Cluster (Kind - Local Dev)        │  │
│  │                                                   │  │
│  │  ┌─────────┐  ┌──────────┐  ┌──────────┐       │  │
│  │  │Control  │  │ Worker   │  │ Worker   │       │  │
│  │  │ Plane   │  │ML Train  │  │ML Infer  │       │  │
│  │  └─────────┘  └──────────┘  └──────────┘       │  │
│  │                                                   │  │
│  │  Persistent Volume: /models (Model Storage)      │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Design Principles

- **Clean Architecture**: Separation of concerns with distinct API, Domain, and Infrastructure layers
- **Domain-Driven Design**: Business logic isolated from framework dependencies
- **Hexagonal Architecture**: Core business rules independent of external systems
- **SOLID Principles**: Testable, maintainable, and extensible code
- **12-Factor App**: Configuration via environment, stateless processes, dev/prod parity

## � Application Layers

The application follows a strict layered architecture where each layer has specific responsibilities and dependencies flow inward:

```text
┌─────────────────────────────────────────────────────────────┐
│                      API LAYER (FastAPI)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ health.py    │  │predictions.py│  │  schemas/       │   │
│  │ /health      │  │ /predict     │  │  (Pydantic DTOs)│   │
│  └──────┬───────┘  └──────┬───────┘  └─────────────────┘   │
│         │                  │                                 │
└─────────┼──────────────────┼─────────────────────────────────┘
          │                  │
          ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    DOMAIN LAYER (Pure Python)                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  RiskScoringService                                  │   │
│  │  • calculate_risk()                                  │   │
│  │  • Business rules (age, BMI, BP scoring)            │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────┐  ┌────────────────┐                       │
│  │HealthMetrics │  │ RiskAssessment │  (Domain Models)     │
│  └──────────────┘  └────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│              INFRASTRUCTURE LAYER                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  ModelLoader                                         │   │
│  │  • load_model() from /models volume                 │   │
│  │  • (Week 5: Load real sklearn/pytorch models)       │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                     CORE LAYER                               │
│  ┌──────────┐  ┌──────────┐  ┌────────────────┐            │
│  │ config.py│  │logging.py│  │ exceptions.py  │            │
│  │(Settings)│  │(JSON logs)│  │(Custom errors) │            │
│  └──────────┘  └──────────┘  └────────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

#### 🌐 API Layer (`app/api/`)
**Purpose**: HTTP interface and request/response handling

- **Routes**: Define REST endpoints (`/health`, `/predict`)
- **Schemas**: Pydantic models for validation and serialization
- **Middleware**: Cross-cutting concerns (CORS, logging, error handling)
- **Dependencies**: FastAPI framework, Pydantic
- **Rules**:
  - No business logic here
  - Only data transformation (DTO ↔ Domain models)
  - Handles HTTP concerns (status codes, headers)

#### 💼 Domain Layer (`app/domain/`)
**Purpose**: Core business logic and rules (framework-agnostic)

- **Services**: `RiskScoringService` - implements risk calculation algorithms
- **Models**: `HealthMetrics`, `RiskAssessment`, `RiskLevel` - domain entities
- **Rules**:
  - Pure Python (no framework imports)
  - Contains all business rules
  - Immutable domain models with validation
  - Can be tested without any external dependencies
  - This is the heart of the application

#### 🏗️ Infrastructure Layer (`app/infrastructure/`)
**Purpose**: External system integrations

- **ML Module**: `ModelLoader` - loads ML models from filesystem/K8s volumes
- **Future**: Database repositories, external APIs, message queues
- **Rules**:
  - Implements interfaces defined by domain layer
  - Handles I/O operations (file, network, database)
  - Can be swapped without changing business logic

#### ⚙️ Core Layer (`app/core/`)
**Purpose**: Cross-cutting technical concerns

- **Config**: Environment-based settings management
- **Logging**: Structured JSON logging for production
- **Exceptions**: Custom exception hierarchy
- **Rules**:
  - Used by all other layers
  - No business logic
  - Only technical utilities

### Dependency Flow

```text
API Layer → Domain Layer → Infrastructure Layer → Core Layer
   ↓             ↓               ↓                    ↓
FastAPI    Pure Python    External I/O         Utilities
(HTTP)     (Business)     (Files, DBs)         (Config)
```

**Key Principle**: Dependencies point inward. The domain layer never imports from API or Infrastructure layers, making it completely framework-independent and easy to test.

## �🚀 Getting Started

### Prerequisites

- Python 3.10+
- Docker Desktop
- kubectl
- Kind (Kubernetes in Docker)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/keniiy/healthwatch-ai.git
   cd healthwatch-ai
   ```

2. **Set up Python environment**

   ```bash
   cd services/health-inference-api
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Create Kubernetes cluster**

   ```bash
   cd ../../infrastructure/kind
   kind create cluster --config kind-ml-cluster.yaml
   ```

### Running Locally

### Option 1: Direct Python (Development)**

```bash
cd services/health-inference-api
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Option 2: Docker (Production-like)

```bash
docker build -t healthwatch-api:latest .
docker run -p 8000:8000 healthwatch-api:latest
```

### Option 3: Kubernetes (Full Stack)

```bash
kubectl apply -f services/health-inference-api/k8s/
```

Access the API at: `http://localhost:8000`

## 📊 Project Structure

```markdown
healthwatch-ai/
├── infrastructure/              # Infrastructure as Code
│   └── kind/
│       ├── kind-ml-cluster.yaml # Kubernetes cluster definition
│       └── models/              # Persistent volume for ML models
│
├── services/
│   └── health-inference-api/    # ML Inference Microservice
│       ├── app/
│       │   ├── api/             # API Layer (Routes, Middleware)
│       │   │   ├── routes/      # Endpoint definitions
│       │   │   └── middleware/  # Request/response processing
│       │   │
│       │   ├── core/            # Core utilities
│       │   │   ├── config.py    # Environment configuration
│       │   │   ├── exceptions.py # Custom exceptions
│       │   │   └── logging.py   # Structured logging
│       │   │
│       │   ├── domain/          # Business Logic (Framework-agnostic)
│       │   │   ├── models/      # Domain entities
│       │   │   │   └── prediction.py # HealthMetrics, RiskAssessment
│       │   │   └── services/    # Business services
│       │   │       └── risk_scorer.py # Risk calculation algorithm
│       │   │
│       │   ├── infrastructure/  # External integrations
│       │   │   └── ml/
│       │   │       └── model_loader.py # ML model management
│       │   │
│       │   └── schemas/         # API DTOs (Pydantic models)
│       │
│       ├── k8s/                 # Kubernetes manifests
│       └── tests/               # Test suites
│           ├── unit/            # Unit tests
│           └── integration/     # Integration tests
│
└── README.md                    # This file
```

## 🔬 API Usage

### Health Risk Assessment Endpoint

**Request:**

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "bmi": 28.5,
    "blood_pressure_systolic": 135
  }'
```

**Response:**

```json
{
  "risk_score": 0.567,
  "risk_level": "MEDIUM",
  "confidence": 0.85,
  "contributing_factors": [
    "Age (45 years) is a significant risk factor",
    "BMI (28.5) indicates overweight",
    "Blood pressure (135 mmHg) is elevated"
  ],
  "timestamp": "2025-10-10T12:34:56.789Z"
}
```

### Risk Levels

| Level | Risk Score Range | Description |
|-------|-----------------|-------------|
| LOW | 0.00 - 0.24 | Minimal health risk |
| MEDIUM | 0.25 - 0.49 | Moderate risk, monitoring recommended |
| HIGH | 0.50 - 0.74 | Significant risk, intervention advised |
| CRITICAL | 0.75 - 1.00 | Severe risk, immediate attention required |

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test suite
pytest tests/unit/
pytest tests/integration/

# Run with verbose output
pytest -v
```

## 🔧 Configuration

Configuration is managed via environment variables (12-factor app methodology):

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | HealthWatch AI - Inference API | Application name |
| `APP_VERSION` | 0.1.0 | API version |
| `DEBUG` | False | Enable debug mode |
| `API_PREFIX` | /api/v1 | API route prefix |
| `MODEL_PATH` | /models | Path to ML models |
| `MODEL_NAME` | health_risk_model.pkl | Model filename |
| `LOG_LEVEL` | INFO | Logging verbosity |
| `HOST` | 0.0.0.0 | Server bind address |
| `PORT` | 8000 | Server port |
| `ENABLE_METRICS` | True | Enable Prometheus metrics |

## 🏗️ Development Roadmap

### Phase 1: MVP (Current) ✅

- [x] Basic API structure with FastAPI
- [x] Clean architecture implementation
- [x] Rule-based risk scoring algorithm
- [x] Kubernetes cluster setup
- [x] Core domain models

### Phase 2: ML Integration (Weeks 3-5)

- [ ] Train actual ML model (scikit-learn/XGBoost)
- [ ] Model serialization and versioning
- [ ] Model loader integration
- [ ] Feature engineering pipeline
- [ ] Model performance monitoring

### Phase 3: Production Readiness (Weeks 6-8)

- [ ] Comprehensive test coverage (>80%)
- [ ] API authentication & authorization
- [ ] Rate limiting and throttling
- [ ] Prometheus metrics export
- [ ] Grafana dashboards
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Docker image optimization
- [ ] Helm charts for deployment

### Phase 4: Advanced Features (Future)

- [ ] Model A/B testing framework
- [ ] Real-time model retraining
- [ ] Multi-model ensemble predictions
- [ ] Patient history tracking
- [ ] Explainable AI (SHAP values)
- [ ] Mobile app integration
- [ ] HIPAA compliance audit

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **API Framework** | FastAPI | High-performance async API |
| **Language** | Python 3.10+ | Core development |
| **ML Framework** | scikit-learn/joblib | Model training & serving |
| **Validation** | Pydantic | Data validation & settings |
| **Logging** | Python logging + structlog | Structured logging |
| **Orchestration** | Kubernetes (Kind) | Container orchestration |
| **Container** | Docker | Application containerization |
| **Testing** | pytest | Unit & integration testing |
| **Code Quality** | ruff, black, mypy | Linting & formatting |
| **Monitoring** | Prometheus + Grafana | Metrics & dashboards |

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Code Standards

- Follow PEP 8 style guide
- Write docstrings for all functions/classes
- Add unit tests for new features
- Maintain >80% code coverage
- Run linters before committing (`ruff`, `black`, `mypy`)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Keniiy**

- GitHub: [@keniiy](https://github.com/keniiy)
- Repository: [healthwatch-ai](https://github.com/keniiy/healthwatch-ai)

## 📚 Documentation

- [API Documentation](docs/api.md) - Detailed API reference
- [Architecture Decision Records](docs/adr/) - Design decisions
- [Deployment Guide](docs/deployment.md) - Production deployment
- [Development Guide](docs/development.md) - Local development setup

## 🙏 Acknowledgments

- FastAPI team for the excellent web framework
- Kubernetes community for orchestration tools
- scikit-learn for ML capabilities
- Clean Architecture principles by Robert C. Martin

## 📧 Support

For questions, issues, or feature requests:

- Open an [issue](https://github.com/keniiy/healthwatch-ai/issues)
- Start a [discussion](https://github.com/keniiy/healthwatch-ai/discussions)

---

Built with ❤️ for better healthcare through AI
