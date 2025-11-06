# 📐 Architecture Documentation

> **Status:** ✅ Production-Ready - Migration Complete (All 7 phases)  
> **Last Updated:** October 3, 2025  
> **Architecture Style:** Clean Architecture with 3-Layer Separation

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Application                       │
│                     (Main Service/External)                      │
└─────────────────┬───────────────────────────────────────────────┘
                  │ gRPC
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    py-microservice                               │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    API Layer (gRPC)                       │  │
│  │  ┌──────────────────┐    ┌──────────────────┐           │  │
│  │  │ Care Planner     │    │ Spelling Check   │           │  │
│  │  │ Servicer         │    │ Servicer         │           │  │
│  │  └────────┬─────────┘    └────────┬─────────┘           │  │
│  └───────────┼──────────────────────┼─────────────────────┘  │
│              │                       │                          │
│  ┌───────────┼──────────────────────┼─────────────────────┐  │
│  │           │   Services Layer     │                      │  │
│  │           ▼                       ▼                      │  │
│  │  ┌──────────────────┐    ┌──────────────────┐          │  │
│  │  │ Care Planner     │    │ Spelling         │          │  │
│  │  │ Service          │    │ Service          │          │  │
│  │  │  - generator.py  │    │  - corrector.py  │          │  │
│  │  │  - planner.py    │    │  - schemas.py    │          │  │
│  │  │  - schemas.py    │    │                  │          │  │
│  │  └────────┬─────────┘    └────────┬─────────┘          │  │
│  └───────────┼──────────────────────┼─────────────────────┘  │
│              │                       │                          │
│  ┌───────────┴───────────────────────┴─────────────────────┐  │
│  │                    Core Layer                            │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │  │
│  │  │ Config   │  │ Logging  │  │ LLM      │             │  │
│  │  │          │  │          │  │ Client   │             │  │
│  │  └──────────┘  └──────────┘  └────┬─────┘             │  │
│  └──────────────────────────────────┼───────────────────┘  │
└─────────────────────────────────────┼───────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────┐
                        │   LLM Service        │
                        │   (OpenRouter)       │
                        └──────────────────────┘
```

## Layer Responsibilities

### 1. API Layer (`src/api/`)

**Responsibility:** Thin gRPC interface layer

- Receives gRPC requests
- Validates request format
- Maps Protobuf ↔ Domain models
- Delegates to service layer
- Handles gRPC-specific errors
- Returns gRPC responses

**Files:**
- `care_planner.py` - CarePlannerServicer
- `spelling_check.py` - SpellingCheckServicer

**Example:**
```python
class CarePlannerServicer:
    def GenerateCarePlan(self, request, context):
        # 1. Map protobuf → domain model
        input_data = self._map_request(request)
        
        # 2. Call service layer
        result = care_planner_service.generate_plan(input_data)
        
        # 3. Map domain model → protobuf
        return self._map_response(result)
```

### 2. Services Layer (`src/services/`)

**Responsibility:** Business logic implementation

- Pure business logic (framework-agnostic)
- LLM interaction
- Data transformation
- Business rule validation
- Can be reused by different API layers (gRPC, REST, etc.)

**Structure:**
```
services/
├── care_planner/
│   ├── planner.py      # Business logic
│   ├── generator.py    # LLM generation
│   └── schemas.py      # Data models
└── spelling/
    ├── corrector.py    # Correction logic
    └── schemas.py      # Data models
```

### 3. Core Layer (`src/core/`)

**Responsibility:** Shared infrastructure

- Configuration management
- Logging setup
- LLM client wrapper
- Custom exceptions
- Cross-cutting concerns

**Files:**
- `config.py` - Environment & app configuration
- `logging.py` - Logging configuration
- `llm_client.py` - LLM client abstraction
- `exceptions.py` - Custom exception classes

## Data Flow

### Request Flow (Care Plan Generation)

```
1. gRPC Request
   └─> src/api/care_planner.py:CarePlannerServicer
       │
       ├─> Validate request
       ├─> Map protobuf to domain model
       │
       └─> src/services/care_planner/planner.py
           │
           ├─> Business logic validation
           │
           └─> src/services/care_planner/generator.py
               │
               ├─> src/core/llm_client.py
               │   └─> LLM API (OpenRouter)
               │
               └─> Format response
                   │
                   └─> Return to API layer
                       │
                       └─> Map to protobuf
                           │
                           └─> gRPC Response
```

### Spelling Correction Flow

```
1. gRPC Request
   └─> src/api/spelling_check.py:SpellingCheckServicer
       │
       └─> src/services/spelling/corrector.py
           │
           └─> src/core/llm_client.py
               └─> LLM API
                   │
                   └─> Corrected text response
```

## Configuration Flow

```
Environment Variables (.env)
    │
    └─> src/core/config.py
        │
        ├─> Application Config
        │   └─> Used by services
        │
        ├─> LLM Config
        │   └─> Used by llm_client.py
        │
        └─> Logging Config
            └─> Used by logging.py
```

## Error Handling Strategy

```
┌──────────────────────────────────────┐
│ API Layer                             │
│  - Catches all exceptions             │
│  - Maps to gRPC status codes         │
│  - Logs errors                        │
└────────────┬─────────────────────────┘
             │
┌────────────▼─────────────────────────┐
│ Service Layer                         │
│  - Raises custom exceptions           │
│  - Business logic validation errors   │
│  - LLM errors                         │
└────────────┬─────────────────────────┘
             │
┌────────────▼─────────────────────────┐
│ Core Layer                            │
│  - Custom exception classes           │
│    • ServiceError                     │
│    • LLMError                         │
│    • ValidationError                  │
│    • ConfigurationError               │
└───────────────────────────────────────┘
```

## Testing Strategy

### Unit Tests (`tests/unit/`)

Test individual components in isolation:

```python
# Test service logic
def test_generate_care_plan():
    service = CarePlannerService()
    result = service.generate_plan(mock_input)
    assert result.is_valid()

# Test utilities
def test_validator():
    assert validate_age(65) == True
    assert validate_age(-1) == False
```

### Integration Tests (`tests/integration/`)

Test gRPC end-to-end:

```python
# Test full gRPC flow
def test_care_planner_grpc(grpc_channel):
    stub = CarePlannerStub(grpc_channel)
    request = create_test_request()
    response = stub.GenerateCarePlan(request)
    assert response.HasField('care_plan_objectives')
```

## Dependency Management

```
┌─────────────────────────────────────┐
│ API Layer                            │
│  Depends on: Services, Core          │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│ Services Layer                       │
│  Depends on: Core                    │
│  Independent of: API                 │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│ Core Layer                           │
│  No dependencies on other layers     │
│  (Infrastructure only)               │
└─────────────────────────────────────┘
```

## Scalability Considerations

### Horizontal Scaling

```
┌────────────┐     ┌────────────┐     ┌────────────┐
│ Service    │     │ Service    │     │ Service    │
│ Instance 1 │     │ Instance 2 │     │ Instance 3 │
└────────────┘     └────────────┘     └────────────┘
      │                   │                   │
      └───────────────────┴───────────────────┘
                          │
                    Load Balancer
```

### Separation of Concerns

Each layer can be:
- Tested independently
- Deployed separately (if needed)
- Scaled independently
- Modified without affecting other layers

## Future Enhancements

### Potential Additions

1. **Caching Layer**
   - Cache LLM responses
   - Redis integration

2. **Message Queue**
   - Async processing
   - RabbitMQ/Kafka integration

3. **Database Layer**
   - Store care plans
   - User history

4. **Monitoring**
   - Metrics collection
   - Performance tracking
   - Health checks

5. **Authentication**
   - API key validation
   - JWT tokens
   - mTLS

```
                    ┌────────────┐
                    │  Clients   │
                    └──────┬─────┘
                           │
                    ┌──────▼─────┐
                    │   API      │
                    │  Gateway   │
                    └──────┬─────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼─────┐      ┌────▼─────┐      ┌────▼─────┐
   │   Auth   │      │  Service │      │  Metrics │
   │ Service  │      │ Instance │      │ Service  │
   └──────────┘      └────┬─────┘      └──────────┘
                          │
                    ┌─────┴─────┐
                    │           │
              ┌─────▼────┐ ┌───▼────┐
              │  Cache   │ │   DB   │
              └──────────┘ └────────┘
```

## Benefits of This Architecture

1. **Separation of Concerns**: Each layer has a single responsibility
2. **Testability**: Easy to test each layer independently
3. **Maintainability**: Clear structure makes code easier to understand
4. **Scalability**: Can scale different components independently
5. **Flexibility**: Easy to swap implementations (e.g., different LLM providers)
6. **Reusability**: Service layer can be used by different API types
7. **Clean Dependencies**: Clear dependency flow (no circular dependencies)
