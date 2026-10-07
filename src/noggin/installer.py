"""Install bundled skills without replacing project-owned content."""

import hashlib
import json
from importlib.resources import files
from pathlib import Path

from noggin import __version__

SKILLS = ("noggin", "noodle", "jot", "ruminate")
STATE = ".agents/noggin.json"
START = "<!-- noggin:start -->"
END = "<!-- noggin:end -->"
BLOCK = f"""{START}
## Noggin memory

Read `noggin/index.md` at the start of project work, then follow relevant links.
Read `noggin/vision.md` when deciding scope and `noggin/principles.md` for rules.
Use the project skills: `$noggin` for memory, `$noodle` for planning, `$jot` for
session capture, and `$ruminate` for reconciling recent work with memory.
Keep indexes current when writing memory. Treat remembered claims as context;
check current code and evidence before relying on them.
{END}
"""


class InstallError(ValueError):
    pass


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def safe_path(root: Path, relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise InstallError(f"Invalid project path: {relative}")
    current = root
    for part in path.parts:
        current /= part
        if current.is_symlink():
            raise InstallError(f"Refusing symlink: {relative}")
    return current


def bundle(directory: str) -> dict[str, bytes]:
    result = {}

    def visit(node, prefix: str = "") -> None:
        for child in sorted(node.iterdir(), key=lambda item: item.name):
            relative = f"{prefix}{child.name}"
            if child.is_dir():
                visit(child, f"{relative}/")
            else:
                result[relative] = child.read_bytes()

    visit(files("noggin").joinpath("resources", directory))
    return result


def load_state(root: Path) -> dict[str, str]:
    path = safe_path(root, STATE)
    if not path.exists():
        return {}
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
        hashes = state["files"]
        if state["schema"] != 1 or state["agent"] != "codex":
            raise ValueError
        if not isinstance(hashes, dict) or not hashes:
            raise ValueError
        for key, value in hashes.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise ValueError
            if not any(key.startswith(f".agents/skills/{s}/") for s in SKILLS):
                raise ValueError
            if len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
                raise ValueError
            safe_path(root, key)
        return hashes
    except (KeyError, ValueError, TypeError) as exc:
        raise InstallError(f"Invalid installation record: {STATE}") from exc


def agent_guide(existing: str) -> str:
    if START not in existing and END not in existing:
        return existing + ("\n\n" if existing else "") + BLOCK
    if existing.count(START) != 1 or existing.count(END) != 1:
        raise InstallError("AGENTS.md has ambiguous noggin markers")
    start, end = existing.index(START), existing.index(END)
    if end < start:
        raise InstallError("AGENTS.md has reversed noggin markers")
    # The project owns this block after installation; preserve local edits.
    return existing


def install(root: Path, *, update: bool = False) -> list[str]:
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise InstallError(f"Project directory does not exist: {root}")
    previous = load_state(root)
    if update and not previous:
        raise InstallError("Noggin is not installed here. Run noggin init first.")

    desired = {
        f".agents/skills/{name}": content for name, content in bundle("skills").items()
    }
    writes: dict[str, bytes] = {}
    conflicts = []
    for relative, content in desired.items():
        target = safe_path(root, relative)
        if target.exists():
            if not target.is_file():
                raise InstallError(f"Expected a file: {relative}")
            current = target.read_bytes()
            if current == content:
                continue
            if not update or digest(current) != previous.get(relative):
                conflicts.append(relative)
                continue
        writes[relative] = content
    if conflicts:
        raise InstallError(
            "Local skill files would be overwritten; reconcile them first:\n"
            + "\n".join(conflicts)
        )

    if not update:
        for relative, content in bundle("scaffold").items():
            name = f"noggin/{relative}"
            target = safe_path(root, name)
            if not target.exists():
                writes[name] = content
            elif not target.is_file():
                raise InstallError(f"Expected a file: {name}")

    guide = safe_path(root, "AGENTS.md")
    existing = guide.read_text(encoding="utf-8") if guide.exists() else ""
    changed = agent_guide(existing)
    if changed != existing:
        writes["AGENTS.md"] = changed.encode()
    state = {
        "schema": 1,
        "agent": "codex",
        "version": __version__,
        "files": {key: digest(value) for key, value in desired.items()},
    }
    encoded = (json.dumps(state, indent=2, sort_keys=True) + "\n").encode()
    state_path = safe_path(root, STATE)
    if not state_path.exists() or state_path.read_bytes() != encoded:
        writes[STATE] = encoded

    directories = [
        "noggin",
        *(f"noggin/{d}" for d in ("wiki", "ledger", "plans", "principles")),
    ]
    if update:
        directories = []
    # Preflight all destinations before making any changes.
    for relative in [*writes, *directories]:
        target = safe_path(root, relative)
        for parent in target.parents:
            if parent == root:
                break
            if parent.exists() and not parent.is_dir():
                raise InstallError(f"Expected a directory: {parent.relative_to(root)}")
        if relative in directories and target.exists() and not target.is_dir():
            raise InstallError(f"Expected a directory: {relative}")
    for relative in directories:
        safe_path(root, relative).mkdir(parents=True, exist_ok=True)
    for relative, content in writes.items():
        target = safe_path(root, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    return list(writes)
