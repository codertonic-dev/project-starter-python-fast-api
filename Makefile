CONTRACT=contracts/openapi.yaml
MODELS=app/company.py

.PHONY: generate run install clean check lint typecheck format pre-commit

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

generate:
	.venv\Scripts\datamodel-codegen.exe --input $(CONTRACT) --input-file-type openapi --output $(MODELS)

run:
	uvicorn app.main:app --reload

check:
	python -c "import app.models" >nul && echo 'Models OK'

lint:
	flake8 app tests

typecheck:
	mypy app

format:
	black app tests
