# Changelog

## Version 1.0.0

- Switched the project to a `uv`-native workflow with `uv_build`, dependency groups, and a refreshed lockfile.
- Modernized `pyproject.toml` metadata and tool configuration for the current package layout.
- Refactored the CLI implementation with stronger typing, centralized constants, and a canonical `alphafold_file_url` helper while keeping backward compatibility for the older misspelled helper name.
- Added explicit typing exports in `affetch.__init__` and `affetch.__version__`.
- Replaced the placeholder test module with executable smoke tests for core parsing and file-writing behavior.
- Rewrote the README, contributing guide, and MkDocs site to focus on real install, usage, development, and reference workflows.

## Version 0.0.1

- First release
