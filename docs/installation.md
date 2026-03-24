# Installation

Run it without installing:

```bash
uvx --from AlphaFoldFetch affetch P11388
```

## Install The CLI

Install AlphaFoldFetch with `uv`:

```bash
uv tool install AlphaFoldFetch
```

This installs the `affetch` command globally.

## Verify

```bash
affetch --help
```

Or:

```bash
uvx --from AlphaFoldFetch affetch --help
```

## Development Setup

For local project work:

```bash
uv sync
uv run pre-commit install
```
