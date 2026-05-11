# Installation

AlphaFoldFetch requires Python 3.11 or newer.

## Run Without Installing

Use `uvx` for a one-off command:

```bash
uvx --from AlphaFoldFetch affetch P11388
```

This is the fastest way to try the CLI.

## Install The CLI

Install AlphaFoldFetch with `uv`:

```bash
uv tool install AlphaFoldFetch
```

Then verify that `affetch` is available:

```bash
affetch --help
```

You can also inspect the help without installing:

```bash
uvx --from AlphaFoldFetch affetch --help
```

## Upgrade

```bash
uv tool upgrade AlphaFoldFetch
```

## Development Install

For local project work:

```bash
uv sync
uv run pre-commit install
```

See [Development](development.md) for test, lint, and docs commands.
