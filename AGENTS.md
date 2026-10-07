# Repository Guidelines

## Project Structure & Module Organization

Noggin is a Python CLI that installs Markdown project memory and four coding
agent skills. Source lives in `src/noggin/`, skill instructions and templates in
`src/noggin/resources/skills/`, and initial memory files in
`src/noggin/resources/scaffold/`. Tests live in `tests/`.

Keep installer behavior separate from Typer command handling. Ship resources
inside the Python package so Git-based `uvx` installation includes them.

## Build, Test, and Development Commands

- `uv sync --locked`: install dependencies from the committed lockfile.
- `uv run noggin --help`: inspect available CLI commands.
- `uv run pytest`: run the installer and CLI tests.
- `uv run ruff check .`: check Python lint rules.
- `uv run ruff format --check .`: verify formatting.
- `uv build`: build the wheel and source distribution.

Run commands from the repository root. Test installation against a temporary
project rather than modifying your own installed skills.

## Coding Style & Naming Conventions

Use Python 3.11-compatible syntax, four-space indentation, type annotations for
public interfaces, and Ruff formatting with an 88-character line limit. Use
`snake_case` for functions and modules and `PascalCase` for classes.

Skill folders match their frontmatter names: `noggin`, `noodle`, `jot`, and
`ruminate`. Use descriptive lowercase hyphenated names for memory documents.
Keep shared memory conventions and templates in the `noggin` skill.

## Testing Guidelines

Use pytest and name tests `test_<behavior>`. Test meaningful installer invariants:
preserved memories and instructions, safe reruns, complete bundled resources,
and conflicts detected before writes. Use `tmp_path` for filesystem tests.
No coverage threshold is configured. For packaging changes, inspect a built
wheel and exercise installation from it.

## Commit & Pull Request Guidelines

Use short, imperative commit subjects and focused commits. Pull requests should
explain the changed behavior, its purpose, and validation performed. Link related
issues when available. Include examples for changes to commands or memory formats.

## Agent Instructions

Use `/Users/alex/.codex/skills/unslop/SKILL.md` for all writing. Read it once per
conversation and preserve factual accuracy and the requested voice and format.
Preserve project-owned memory and locally edited skills during installer changes.
Keep credentials, generated build output, and local environments out of Git.
