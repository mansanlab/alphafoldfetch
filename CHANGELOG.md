# Changelog

## Version 1.0.2

- Tightened CLI validation for file types, output paths, and download/write concurrency options.
- Improved FASTA input handling for uppercase suffixes and cleaner missing-file errors.
- Surfaced structure write failures from worker threads instead of allowing them to be ignored.
- Reduced URL batching memory use by chunking iterables directly.

## Version 1.0.1

- Updated github pages to compile correctly after removing some GitHub Actions.

## Version 1.0.0

- Switched the project to a `uv`-native workflow with `uv_build`, dependency groups, and a refreshed lockfile.
- Modernized `pyproject.toml` metadata and tool configuration for the current package layout.
- Refactored the CLI implementation with stronger typing, centralized constants, and a canonical `alphafold_file_url` helper while keeping backward compatibility for the older misspelled helper name.
- Added explicit typing exports in `affetch.__init__` and `affetch.__version__`.
- Replaced the placeholder test module with executable smoke tests for core parsing and file-writing behavior.
- Rewrote the README, contributing guide, and MkDocs site to focus on real install, usage, development, and reference workflows.

## Version 0.0.1

- First release
