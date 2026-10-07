# Repository Guidelines

## Project Structure & Module Organization

This repository is currently a new Git workspace with no application code or established directory layout. When adding the first implementation, group source code by feature or responsibility, place tests alongside the code or in a dedicated `tests/` directory, and keep static assets separate. Document the chosen layout in `README.md`. Avoid introducing empty directories solely to match a template.

## Build, Test, and Development Commands

No build system, dependency manifest, or development commands are configured yet. When selecting a toolchain, add reproducible commands for installing dependencies, running locally, building, and testing to `README.md`. Commit the appropriate dependency lockfile. Run commands from the repository root unless the documentation specifies another directory.

## Coding Style & Naming Conventions

Follow the chosen language’s standard formatter and naming conventions. Configure indentation, formatting, and linting before adding substantial code. Use descriptive names, keep modules focused, and match existing conventions as they emerge. Avoid unrelated formatting changes in functional patches.

## Testing Guidelines

No testing framework or coverage threshold is established. Add tests for new behavior and bug fixes using the selected framework’s discovery conventions. Keep tests deterministic and document any required services or fixtures. Record the test command and results in pull requests.

## Commit & Pull Request Guidelines

There is no commit history from which to infer a message convention. Use short, imperative subjects, such as `Add initial application scaffold`, and keep commits focused. Pull requests should explain the change, its purpose, and validation performed. Link relevant issues and include screenshots when changing visible interfaces.

## Security & Configuration

Keep credentials and local configuration out of Git. Provide example configuration with placeholder values when needed, and add generated files to `.gitignore`.

## Agent Instructions

Use `/Users/alex/.codex/skills/unslop/SKILL.md` for all writing. Read it once per conversation and preserve factual accuracy and the requested voice and format.
