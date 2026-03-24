# Development

## Setup

Install project dependencies with `uv`:

```bash
uv sync
```

Install pre-commit hooks once:

```bash
uv run pre-commit install
```

## Main Commands

Run tests:

```bash
uv run pytest
```

Run lint checks:

```bash
uv run ruff check .
uv run ruff format --check .
```

Run type checks:

```bash
uv run mypy affetch tests
```

Inspect the CLI:

```bash
uv run affetch --help
```

## Docs Workflow

Serve docs locally:

```bash
uv run --group docs mkdocs serve --config-file mkdocs.yml --dev-addr localhost:8000
```

Build docs in strict mode:

```bash
uv run --group docs mkdocs build --config-file mkdocs.yml --clean --strict
```

## Project Layout

- `affetch/`: package source
- `tests/`: test suite
- `docs/`: documentation site
- `pyproject.toml`: package metadata and tooling configuration
