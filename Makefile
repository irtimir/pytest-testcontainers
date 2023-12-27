SHELL:=/usr/bin/env bash

.PHONY: lint
lint:
	poetry run mypy pytest_testcontainers tests/**/*.py
	poetry run flake8 pytest_testcontainers
	poetry run flake8 tests
	if poetry run command -v doc8 > /dev/null 2>&1; then poetry run doc8 -q docs; fi

.PHONY: unit
unit:
	poetry run pytest --pdb tests

.PHONY: package
package:
	poetry check
	poetry run pip check
	poetry run safety check --full-report

.PHONY: test
test: lint package unit
