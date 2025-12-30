# FastAPI Contract-First Starter

[![npm](https://img.shields.io/npm/v/@openapitools/openapi-generator-cli)](https://www.npmjs.com/package/@openapitools/openapi-generator-cli)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/github/license/your-org/fastapi-contract-first)](LICENSE)

Contract-first FastAPI project starter using OpenAPI Generator. Define APIs in YAML spec → Generate server stubs → Implement business logic separately.

## 🎯 Features

- ✅ **Contract-First**: OpenAPI YAML as single source of truth
- ✅ **Auto-Generated**: FastAPI routers + Pydantic models from spec
- ✅ **Safe Regeneration**: Generated code isolated in `/generated`
- ✅ **Cross-Platform**: Windows/Mac/Linux (npm + Java 21)
- ✅ **Pre-commit**: Spec validation + formatting
- ✅ **Production-Ready**: Type-safe, documented APIs

## 📁 Project Structure

fastapi-contract-first/
├── package.json # npm scripts (generate, validate)
├── requirements.txt # Python deps
├── .pre-commit-config.yaml
├── app/ # 🟢 Custom implementation (never regenerate)
│ ├── main.py # App bootstrap + wiring
│ ├── api/impl/ # 🔴 Business logic
│ └── core/config.py
├── generated/ # 🟡 Generated (delete + regenerate)
│ ├── main.py
│ ├── api/default/
│ └── models/
├── openapi/specs/ # 📄 API Contracts
│ └── service.yaml
└── tests/


## 🚀 Quick Start

### Prerequisites

1. Python 3.11+
python --version

2. Node.js + npm
node -v # v20+
npm -v # 10+

3. Java 21+ (for OpenAPI Generator)
java -version # openjdk 21+


### Setup (Windows Command Prompt)
git clone <repo>
cd fastapi-contract-first

REM Node deps
npm install

REM Python virtualenv
python -m venv .venv
.venv\Scripts\activate

REM Python deps
pip install -r requirements.txt

REM Generate API stubs
npm run generate:full

REM Install pre-commit hooks
pre-commit install

REM Run server
uvicorn app.main:app --reload


**Test:** `http://localhost:8000/api/v1/health` → `{"status": "ok"}`

## 🔄 Contract-First Workflow

📝 Edit → openapi/specs/service.yaml

✅ Validate → npm run validate-spec

⚡ Generate → npm run generate:full

💻 Implement → app/api/impl/*.py

🧪 Test → pytest

🚀 Run → uvicorn app.main:app --reload



### Example: Add Person Entity

**1. Edit spec** (`openapi/specs/service.yaml`):
paths:
/persons:
post:
operationId: createPerson
...

**2. Regenerate**:
npm run generate:full

**3. Implement** (`app/api/impl/person.py`):
def create_person(person: PersonCreate) -> Person:
return Person(id="p-123", name=person.name, email=person.email)

**4. Restart server** → New `/api/v1/persons` endpoint ready!

## 📦 NPM Scripts

| Command | Description |
|---------|-------------|
| `npm run generate:full` | Clean + generate API stubs |
| `npm run generate` | Generate from spec |
| `npm run clean` | Delete `/generated` |
| `npm run validate-spec` | Lint OpenAPI YAML |

## 🐍 Python Commands

.venv\Scripts\activate # Activate virtualenv
pip install -r requirements.txt # Install deps
uvicorn app.main:app --reload # Dev server
pytest # Run tests

## 👥 Team Onboarding (Party, Company, etc.)

1. **Copy starter** → `party-service/`, `company-service/`
2. **Rename spec** → `openapi/specs/party.yaml`
3. **Update contract** → Add domain endpoints
4. **`npm run generate:full`** → Domain-specific stubs ready
5. **Implement** → `app/api/impl/party.py`

## ⚠️ Important Rules

| ✅ DO | ❌ NEVER |
|------|----------|
| Edit `openapi/specs/*.yaml` | Edit `/generated/*` |
| `npm run generate:full` | Hand-write FastAPI routes |
| Implement in `app/api/impl/` | Commit generated code |
| Use generated Pydantic models | Ignore spec validation |

## 🛠 Developer Tooling

- **Pre-commit**: Spectral linting, Black, isort
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health checks**: `/api/v1/health`

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `java` not found | `winget install EclipseAdoptium.Temurin.21.JDK` |
| `npm` policy error | Use **Command Prompt** (not PowerShell) |
| Spec validation | Add `description` to all responses |
| `uvicorn` not found | `.venv\Scripts\activate` + `pip install "fastapi[standard]"` |

## 📄 Requirements

**requirements.txt:**
fastapi[standard]
pydantic[email]
httpx
pytest

## 🤝 Contributing

1. Branch: `feat/person-endpoints`
2. Update `openapi/specs/service.yaml`
3. `npm run generate:full`
4. Add tests → `pytest`
5. `git commit` (pre-commit runs automatically)

## 📈 Generated Clients

Generate client SDKs from same spec:
npm run generate:client # typescript-fetch
npm run generate:client:go # go
npm run generate:client:js # javascript

## License

MIT © Codertonic
