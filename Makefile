CONTRACT=contracts/openapi.yaml
MODELS=app/model.py

.PHONY: install generate run check lint typecheck format test clean dev

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

generate:
	.venv/Scripts/datamodel-codegen.exe \
		--input $(CONTRACT) \
		--input-file-type openapi \
		--output $(MODELS)
	.venv/bin/datamodel-codegen --input $(CONTRACT) --input-file-type openapi --output $(MODELS)

run:
	.venv/Scripts/uvicorn.exe app.main:app --reload --host 0.0.0.0 --port 8000

check:
	python -c "import app.models; print('✅ Models OK')"

lint:
	flake8 app tests

typecheck:
	mypy app

format:
	black app tests

test:
	pytest tests/ -v

dev:
	make install && make generate && make check && make run
