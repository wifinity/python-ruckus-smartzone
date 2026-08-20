# vim:ft=make:noexpandtab:
PYTHON ?= python3
.PHONY: format format-check lint type-check unit-tests tests test \
	spec-fetch spec-fetch-controller generate-models spec-validate venv help
.DEFAULT_GOAL := help

format: ## Run black formatter
	uv run black .

format-check: ## Check black formatting
	@echo "Running black"
	uv run black --check --diff .

lint: format-check ## Run linter
	@echo "Running flake8"
	uv run flake8 ruckus_smartzone/ tools/ --format=github

type-check: ## Run type checks
	@echo "Running mypy"
	uv run mypy ruckus_smartzone --explicit-package-bases --show-error-codes --error-summary

unit-tests: ## Run unit tests
	@echo "Running pytest"
	uv run pytest -v -s tests/

tests: lint type-check unit-tests ## Run all tests
test: tests

spec-fetch: ## Fetch the SmartZone spec + manifest (pass args via SPEC_FETCH_ARGS)
	uv run $(PYTHON) tools/fetch_spec.py $(SPEC_FETCH_ARGS)

spec-fetch-controller: ## Fetch from a controller (set SMARTZONE_BASE_URL; address not stored in repo)
	@test -n "$(SMARTZONE_BASE_URL)" || { echo "SMARTZONE_BASE_URL is required (e.g. https://<controller>:8443)"; exit 1; }
	uv run $(PYTHON) tools/fetch_spec.py --base-url "$(SMARTZONE_BASE_URL)" --insecure

generate-models: ## Generate the internal schema index from the fetched spec
	uv run $(PYTHON) tools/generate_models.py

spec-validate: ## Validate the fetched spec
	uv run $(PYTHON) tools/validate_spec.py

venv: ## Create venv
	test -d .venv || uv venv
	uv pip install -r requirements.txt -r requirements-dev.txt

help: ## Show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'
