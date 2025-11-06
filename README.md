# py-microservice

A Python-based gRPC microservice for LLM communication, providing care planning and spelling correction services.

## 📋 Overview

This microservice handles LLM (Large Language Model) communication for the main service over gRPC. It provides two main services:

1. **Care Planner Service**: Generates personalized care plans using LLM
2. **Spelling Correction Service**: Corrects spelling using LLM-powered correction

## 🏗️ Architecture

```
py-microservice/
├── src/                      # Source code
│   ├── api/                 # gRPC service implementations
│   ├── services/            # Business logic
│   ├── core/                # Configuration & shared utilities
│   ├── models/              # Domain models
│   └── utils/               # Helper functions
├── generated/               # Auto-generated gRPC code
├── proto/                   # Protocol buffer definitions
├── tests/                   # Tests (unit & integration)
├── scripts/                 # Utility scripts
└── logs/                    # Application logs
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- Protocol Buffers compiler

### Setup

```bash
# 1. Clone the repository
git clone <repository-url>
cd py-microservice

# 2. Run setup script
./scripts/setup_dev.sh

# 3. Configure environment
cp .env.example .env
# Edit .env with your configuration (especially OPENROUTER_API_KEY)

# 4. Generate proto files (if not done by setup script)
./scripts/generate_protos.sh
```

### Running the Service

```bash
# Using Make
make run

# Or directly with Python
python main.py
```

### Running Tests

```bash
# Run all tests
make test

# Run unit tests only
pytest tests/unit/

# Run integration tests only
pytest tests/integration/

# Run with coverage
make test-cov
```

## 🔧 Development

### Project Structure

```
src/
├── api/                          # Thin gRPC layer
│   ├── care_planner.py          # Care planner gRPC servicer
│   └── spelling_check.py        # Spelling check gRPC servicer
│
├── services/                     # Business logic
│   ├── care_planner/
│   │   ├── planner.py           # Care plan business logic
│   │   ├── generator.py         # LLM generation
│   │   └── schemas.py           # Pydantic models
│   └── spelling/
│       ├── corrector.py         # Spelling correction logic
│       └── schemas.py           # Pydantic models
│
└── core/                         # Shared infrastructure
    ├── config.py                # Application configuration
    ├── logging.py               # Logging setup
    ├── llm_client.py            # LLM client wrapper
    └── exceptions.py            # Custom exceptions
```

### Key Technologies

- **gRPC**: High-performance RPC framework
- **Protocol Buffers**: Interface definition language
- **Pydantic**: Data validation using Python type annotations
- **pydantic-ai**: LLM interaction framework
- **pytest**: Testing framework

### Code Quality

```bash
# Format code
make format

# Lint code
make lint

# Type check
make type-check
```

## 📡 gRPC Services

### Care Planner Service

Generates personalized care plans based on client data and assessment results.

**RPC Methods:**
- `GenerateCarePlan`: Creates a care plan with short-term, medium-term, and long-term goals

### Spelling Correction Service

Provides LLM-powered spelling correction for text input.

**RPC Methods:**
- `CorrectSpelling`: Corrects spelling errors in provided text

## 🔐 Configuration

Configuration is managed through environment variables. See `.env.example` for all available options.

### Required Environment Variables

```bash
OPENROUTER_API_KEY=your_api_key_here  # Required for LLM communication
ENVIRONMENT=development               # Environment (development/staging/production)
LOG_LEVEL=INFO                       # Logging level
GRPC_PORT=50051                      # gRPC server port
GRPC_MAX_WORKERS=4                   # Number of worker threads
```

## 🧪 Testing

### Test Organization

```
tests/
├── unit/                    # Unit tests (isolated components)
├── integration/             # Integration tests (gRPC end-to-end)
├── fixtures/                # Test fixtures and factories
└── conftest.py             # Pytest configuration
```

### Writing Tests

```python
# Unit test example
def test_generate_care_plan():
    result = generate_care_plan(sample_input)
    assert result.client_profile.age == 65

# Integration test example
def test_grpc_care_planner(grpc_stub):
    request = pb2.PersonalizedCarePlanRequest(...)
    response = grpc_stub.GenerateCarePlan(request)
    assert response.assessment_summary
```

## 🐳 Docker

### Build Image

```bash
docker build -t py-microservice .
```

### Run Container

```bash
docker run -p 50051:50051 \
  -e OPENROUTER_API_KEY=your_key \
  py-microservice
```

## 📊 Logging

Logs are written to both console and file (`logs/app.log`). Log level can be configured via `LOG_LEVEL` environment variable.

**Log Levels:** DEBUG, INFO, WARNING, ERROR, CRITICAL

## 🔄 Migration Status

This project has successfully completed a full restructuring from an MVP to a production-ready microservice architecture. See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for details on the migration process.

**Status:** ✅ **Migration Complete** (All 7 phases completed)

### Migration Phases Completed:
- ✅ Phase 1: Structure Creation
- ✅ Phase 2: Core Configuration
- ✅ Phase 3: Services Migration
- ✅ Phase 4: API Layer
- ✅ Phase 5: Tests Migration
- ✅ Phase 6: Cleanup
- ✅ Phase 7: Final Verification

The codebase now follows clean architecture principles with clear separation of concerns, comprehensive testing, and production-ready structure.

## 🛠️ Makefile Commands

```bash
make help          # Show all available commands
make run           # Start the gRPC server
make test          # Run all tests
make test-cov      # Run tests with coverage
make lint          # Run linters
make format        # Format code
make proto         # Generate proto files
make clean         # Clean generated files
```

## 📝 Development Workflow

1. Create a feature branch
2. Make changes
3. Write/update tests
4. Run tests: `make test`
5. Format code: `make format`
6. Lint code: `make lint`
7. Commit and push
8. Create pull request

## 🤝 Contributing

1. Follow the existing code structure
2. Write tests for new features
3. Update documentation
4. Follow Python best practices (PEP 8)
5. Use type hints

## 📄 License

[Add your license here]

## 📞 Support

[Add contact information or issue tracker link]

---

**Note:** This microservice has been fully restructured with clean architecture, comprehensive testing, and production-ready code organization. See phase completion documents (PHASE_*_COMPLETE.md) for detailed migration history.
