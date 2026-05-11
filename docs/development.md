# Development

Use this page when working on AlphaFoldFetch locally.

## Setup

Install dependencies:

```bash
uv sync
```

Install pre-commit hooks once:

```bash
uv run pre-commit install
```

## Check Your Work

Run tests:

```bash
uv run pytest
```

Run lint and formatting checks:

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

## Docs

Serve the docs locally:

```bash
uv run --group docs mkdocs serve --config-file mkdocs.yml --dev-addr localhost:8000
```

Build the docs in strict mode:

```bash
uv run --group docs mkdocs build --config-file mkdocs.yml --clean --strict
```

## Project Layout

| Path | Purpose |
| --- | --- |
| `affetch/` | Package source |
| `tests/` | Test suite |
| `docs/` | Documentation site |
| `pyproject.toml` | Package metadata and tool configuration |
