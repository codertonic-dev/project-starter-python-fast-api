# FastAPI Contract-First Starter

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/github/license/your-org/fastapi-contract-first)](LICENSE)

Contract-first FastAPI project starter using datamodel-code-generator. Define APIs in YAML spec → Generate Pydantic models → Implement business logic with clean architecture.

## 🎯 Features

- ✅ **Contract-First**: OpenAPI YAML as single source of truth
- ✅ **Auto-Generated**: Pydantic models from spec
- ✅ **Clean Architecture**: Service layer with dependency injection
- ✅ **Cross-Platform**: Windows/Mac/Linux (Python + Make)
- ✅ **Pre-commit**: Code formatting and linting
- ✅ **Production-Ready**: Type-safe, documented APIs with unit tests

## 📁 Project Structure

```
project-starter-python-fast-api/
├── Makefile              # Build and development commands
├── requirements.txt      # Python dependencies
├── pytest.ini           # Pytest configuration
├── .pre-commit-config.yaml
├── contracts/            # 📄 API Contracts
│   └── openapi.yaml
├── app/                  # 🟢 Custom implementation
│   ├── main.py          # App bootstrap + routing
│   ├── models.py        # 🟡 Generated Pydantic models
│   ├── api/             # API route handlers
│   │   ├── health.py
│   │   └── persons.py
│   └── services/        # Business logic layer
│       ├── health_service.py
│       ├── health_impl.py
│       ├── person_service.py
│       └── persons_impl.py
└── tests/               # Unit tests
    ├── test_health.py
    └── test_persons.py
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.11+**
   ```bash
   python --version
   ```

### Setup

```bash
# Clone the repository
git clone <repo>
cd project-starter-python-fast-api

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
make install
# Or manually:
pip install -r requirements.txt

# Generate models from OpenAPI spec
make generate

# Install pre-commit hooks (optional)
pre-commit install

# Run the server
make run
# Or manually:
uvicorn app.main:app --reload
```

**Test:** `http://localhost:8000/api/v1/health` → `{"status": "ok"}`

## 🔄 Contract-First Workflow

1. 📝 **Edit** → `contracts/openapi.yaml`
2. ⚡ **Generate** → `make generate` (regenerates `app/models.py`)
3. 💻 **Implement** → Add service interfaces in `app/services/*_service.py`
4. 🔧 **Implement** → Add service implementations in `app/services/*_impl.py`
5. 🛣️ **Wire** → Add API routes in `app/api/*.py`
6. 🧪 **Test** → `pytest`
7. 🚀 **Run** → `make run`

### Example: Add Person Entity

**1. Edit spec** (`contracts/openapi.yaml`):
```yaml
paths:
  /persons:
    post:
      operationId: createPerson
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PersonCreate'
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Person'
```

**2. Regenerate models:**
```bash
make generate
```

**3. Create service interface** (`app/services/person_service.py`):
```python
from abc import ABC, abstractmethod
from app.models import PersonCreate, Person

class PersonService(ABC):
    @abstractmethod
    async def create_person(self, data: PersonCreate) -> Person:
        raise NotImplementedError
```

**4. Implement service** (`app/services/persons_impl.py`):
```python
from app.services.person_service import PersonService
from app.models import PersonCreate, Person

class PersonServiceImpl(PersonService):
    async def create_person(self, data: PersonCreate) -> Person:
        # Your business logic here
        return Person(id="p-123", **data.model_dump())
```

**5. Create API route** (`app/api/persons.py`):
```python
from fastapi import APIRouter, Depends
from app.services.person_service import PersonService
from app.services.persons_impl import PersonServiceImpl

router = APIRouter()

def get_person_service() -> PersonService:
    return PersonServiceImpl()

@router.post("/persons", response_model=Person, status_code=201)
async def create_person_endpoint(
    data: PersonCreate,
    service: PersonService = Depends(get_person_service),
) -> Person:
    return await service.create_person(data)
```

**6. Register route** (`app/main.py`):
```python
from app.api.persons import router as persons_router
app.include_router(persons_router, prefix="/api/v1")
```

## 📦 Make Commands

| Command | Description |
|---------|-------------|
| `make install` | Install Python dependencies |
| `make generate` | Generate Pydantic models from OpenAPI spec |
| `make run` | Start development server |
| `make lint` | Run flake8 linter |
| `make typecheck` | Run mypy type checker |
| `make format` | Format code with Black |
| `make check` | Verify models can be imported |

## 🐍 Python Commands

```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload

# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/
```

## 🧪 Testing

Run all tests:
```bash
pytest tests/ -v
```

Run specific test file:
```bash
pytest tests/test_persons.py -v
```

## 🛠 Developer Tooling

- **Pre-commit**: Black, flake8, mypy, pylint
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health check**: `http://localhost:8000/api/v1/health`
- **Persons API**: `http://localhost:8000/api/v1/persons`

## ⚠️ Important Rules

| ✅ DO | ❌ NEVER |
|------|----------|
| Edit `contracts/openapi.yaml` | Edit `app/models.py` directly |
| Run `make generate` after spec changes | Hand-write Pydantic models |
| Implement in `app/services/` | Put business logic in API routes |
| Use service interfaces | Skip dependency injection |
| Write unit tests | Skip testing |

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `datamodel-codegen` not found | Run `make install` or `pip install -r requirements.txt` |
| `uvicorn` not found | Activate venv: `source .venv/bin/activate` |
| Import errors | Run `make generate` to regenerate models |
| Tests fail | Ensure `pytest` and `pytest-asyncio` are installed |

## 📄 Requirements

Key dependencies:
- `fastapi` - Web framework
- `uvicorn[standard]` - ASGI server
- `datamodel-code-generator` - Generate models from OpenAPI
- `pydantic[email]` - Data validation
- `pytest` & `pytest-asyncio` - Testing framework
- `black`, `mypy`, `flake8` - Code quality tools

See `requirements.txt` for full list.

## 🤝 Contributing

1. Create branch: `feat/new-endpoint`
2. Update `contracts/openapi.yaml`
3. Run `make generate`
4. Implement service interface and implementation
5. Add API route
6. Write unit tests
7. Run `make lint` and `make typecheck`
8. Commit (pre-commit runs automatically)

## License

MIT © Codertonic
