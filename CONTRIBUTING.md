# Contributing

Thanks for helping improve AlphaFoldFetch.

This project is small and CLI-focused, so the most helpful contributions are usually one of these:

- bug fixes
- better tests
- clearer docs
- usability improvements to the CLI

## Before You Start

For non-trivial changes, open an issue first so the implementation direction is clear before you spend time on it.

Use the issue tracker for:

- bug reports
- feature requests
- docs problems
- behavior questions

When reporting a bug, include:

- your OS
- your Python version
- the command you ran
- a small reproducible example
- the error output, if there is one

## Local Setup

Clone the repository and install dependencies with `uv`:

```console
git clone git@github.com:YourLogin/alphafoldfetch.git
cd alphafoldfetch
uv sync
uv run pre-commit install
```

## Development Workflow

Create a branch for your work:

```console
git switch --create my-change
```

Useful local commands:

```console
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy affetch tests
uv run affetch --help
```

If you change the docs, you can preview them locally:

```console
uv run --group docs mkdocs serve --config-file mkdocs.yml --dev-addr localhost:8000
```

Build the docs in strict mode:

```console
uv run --group docs mkdocs build --config-file mkdocs.yml --clean --strict
```

## Pull Requests

Before opening a pull request:

- keep the change focused
- add or update tests when behavior changes
- update docs when the CLI behavior changes
- run the local checks listed above

Then commit and push your branch:

```console
git add <files>
git commit
git push --set-upstream origin my-change
```

Open a pull request from your fork and include a short explanation of:

- what changed
- why it changed
- how you tested it

## Docs Contributions

Docs changes are welcome on their own. If the improvement is clear and self-contained, a documentation-only pull request is completely fine.
