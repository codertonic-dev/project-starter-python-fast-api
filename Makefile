SPEC_PATH=openapi/specs/service.yaml
GENERATED_PATH=generated
NPM_GENERATOR=openapi-generator-cli

generate: clean-generated install-generator
	npm run generate

validate-spec:
	npx spectral lint $(SPEC_PATH)

format:
	npx black .
	npx isort .

clean-generated:
	rm -rf $(GENERATED_PATH)
	mkdir -p $(GENERATED_PATH)

install-generator:
	npm install -g $(NPM_GENERATOR)

.PHONY: generate validate-spec format clean-generated install-generator
