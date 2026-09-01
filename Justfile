test: test-pytest
lint: lint-ruff lint-mypy
fmt: fmt-ruff lint-ruff-fix
pre-publish: clean sync fmt lint test build

run +args:
    uv run crestic {{args}}

debug +args:
    - env CRESTIC_DRYRUN=1 uv run crestic {{args}}

clean:
    - rm -rf dist/*

build:
    uv build

publish: pre-publish
    uv publish

sync:
    uv sync

fmt-ruff:
    uv run ruff format

lint-ruff:
    uv run ruff check

lint-ruff-fix:
    uv run ruff check --fix

lint-pyrefly:
    uv run pyrefly check

lint-mypy:
    uv run mypy .

test-pytest:
    uv run pytest
