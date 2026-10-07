# noggin

A little project memory for coding agents. Noggin is a personal engineering
experiment: Markdown files you can inspect, edit, and version, plus four skills
that help an agent use and maintain them.

## Install

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/).

### Install the noggin command

Install once to use `noggin` directly from your terminal:

```sh
uv tool install git+https://github.com/alexph/noggin
```

Then, from any project's root:

```sh
noggin init
```

uv keeps the tool and its dependencies in an isolated environment, separate
from your projects. If `noggin` is not found after installation, run
`uv tool update-shell` and restart your shell. See [uv's tool installation guide](https://docs.astral.sh/uv/guides/tools/#installing-tools).

To install from a local checkout before pushing to GitHub, run this from the
Noggin repository root:

```sh
uv tool install .
```

### Run without a persistent installation

Alternatively, run from your project's root using `uvx`:

```sh
uvx --from git+https://github.com/alexph/noggin noggin init
```

Choose `codex` when prompted, or pass `--agent codex`. Use `--path /path/to/project`
to target another directory. Codex is the first supported agent. The command
installs project-local skills in `.agents/skills/`, creates `noggin/`, and appends
a marked section to `AGENTS.md`, preserving existing instructions. The skill
location follows the [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills).

The GitHub commands require this implementation to be pushed first. To try the
current checkout without publishing:

```sh
uv run noggin init --agent codex --path /path/to/project
```

## Memory layout

```text
noggin/
    index.md          # Curated entry point
    vision.md         # Purpose, goals, scope, non-goals
    principles.md     # Semantic index of durable rules
    wiki/             # Current project knowledge
    ledger/           # Completed work, decisions, outcomes
    plans/            # Backlog and actionable plans
    principles/       # Rules, rationale, scope, evidence
```

Indexes group links under meaningful headings, with short descriptions:

```markdown
## Core

- [[principles/boundaries]] — Module ownership and dependency rules.
```

Wiki links resolve from `noggin/`, with `.md` optional. Whole-document links are
supported by convention; Markdown viewers without wiki-link support will show
the source syntax. Noggin does not require a particular editor or wiki renderer.

## The skills

| Skill | Use it for |
| --- | --- |
| `noggin` | Finding knowledge and maintaining memory |
| `noodle` | Planning work, affected areas, subtasks, risks, and verification |
| `jot` | Capturing useful discoveries from the current session |
| `ruminate` | Reconciling recent changes or supplied sessions with memory |

Try asking Codex: “Use `$noodle` to plan this change,” “Use `$jot` to capture
what we learned,” or “Use `$ruminate` to review the last five commits.”

The skills share templates shipped inside the `noggin` skill. Plans, ledger
entries, principles, and vision have predictable sections; wiki pages have a
flexible body. Optional empty sections are omitted. Memories retain evidence
and uncertainty, and existing pages are updated before duplicate pages are added.
The CLI installs files; the agent performs memory collection. It does not call
a model, run a background collector, or automatically read session logs.

## Updating

Run the current package's `noggin update`, for example:

```sh
uvx --from git+https://github.com/alexph/noggin noggin update
```

Updates refresh bundled skill files only when their contents match the last
installed version. Edited or unrelated skills cause an error before any writes;
reconcile those files before retrying. Project memories, extra skill files, and
existing agent instructions are preserved. `.agents/noggin.json` records installed
file hashes and should travel with the skills. Initialization is safe to rerun:
it fills missing scaffold files and directories without replacing memories.

## Development

Python 3.11 or newer. Use the committed lockfile:

```sh
uv sync --locked
uv run noggin --help
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv build
```

Python lives in `src/noggin/`; bundled skills and scaffolds live in
`src/noggin/resources/`; tests live in `tests/`. Tests exercise installation,
repeat runs, upgrades, conflict preservation, CLI selection, and resource loading.
