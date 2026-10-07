import hashlib
import json
from pathlib import Path

import pytest
import yaml
from typer.testing import CliRunner

from noggin.cli import app
from noggin.installer import END, SKILLS, START, STATE, InstallError, bundle, install


def snapshot(root: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def test_init_installs_bundle_and_is_idempotent(tmp_path):
    guide = tmp_path / "AGENTS.md"
    guide.write_text("# Existing rules\n\nKeep this.\n")
    install(tmp_path)
    first = snapshot(tmp_path)
    assert guide.read_text().startswith("# Existing rules\n\nKeep this.\n")
    assert guide.read_text().count(START) == 1
    for skill in SKILLS:
        assert (tmp_path / f".agents/skills/{skill}/SKILL.md").is_file()
    for directory in ("wiki", "ledger", "plans", "principles"):
        assert (tmp_path / "noggin" / directory).is_dir()
    assert install(tmp_path) == []
    assert snapshot(tmp_path) == first


def test_preserve_memories_and_guide(tmp_path):
    install(tmp_path)
    for name in ("vision.md", "principles.md", "index.md", "wiki/details.md"):
        (tmp_path / "noggin" / name).write_text("Personal memory\n")
    guide = tmp_path / "AGENTS.md"
    guide.write_text(
        guide.read_text().replace("Read `noggin/index.md`", "Consult my index")
    )
    before = snapshot(tmp_path)
    install(tmp_path)
    install(tmp_path, update=True)
    assert snapshot(tmp_path) == before


@pytest.mark.parametrize("update", [False, True])
def test_local_skill_conflict_has_no_partial_writes(tmp_path, update):
    install(tmp_path)
    (tmp_path / ".agents/skills/jot/SKILL.md").write_text("My edited skill\n")
    (tmp_path / ".agents/skills/noodle/SKILL.md").unlink()
    before = snapshot(tmp_path)
    with pytest.raises(InstallError, match="Local skill"):
        install(tmp_path, update=update)
    assert snapshot(tmp_path) == before


def test_update_replaces_previously_shipped_content(tmp_path):
    install(tmp_path)
    key = ".agents/skills/jot/SKILL.md"
    old = b"An earlier bundled version\n"
    (tmp_path / key).write_bytes(old)
    state_path = tmp_path / STATE
    state = json.loads(state_path.read_text())
    state["files"][key] = hashlib.sha256(old).hexdigest()
    state_path.write_text(json.dumps(state))
    assert key in install(tmp_path, update=True)
    assert (tmp_path / key).read_bytes() == bundle("skills")["jot/SKILL.md"]


def test_unknown_skill_is_not_overwritten(tmp_path):
    target = tmp_path / ".agents/skills/noodle/SKILL.md"
    target.parent.mkdir(parents=True)
    target.write_text("Unrelated noodle skill\n")
    before = snapshot(tmp_path)
    with pytest.raises(InstallError, match="Local skill"):
        install(tmp_path)
    assert snapshot(tmp_path) == before


@pytest.mark.parametrize("relative", ["noggin", ".agents", "AGENTS.md"])
def test_symlinks_are_rejected_before_writing(tmp_path, relative):
    project = tmp_path / "project"
    project.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (project / relative).symlink_to(outside)
    with pytest.raises(InstallError, match="symlink"):
        install(project)
    assert list(outside.iterdir()) == []
    assert not (project / STATE).exists()


@pytest.mark.parametrize("relative", ["noggin/wiki", ".agents/skills", "AGENTS.md"])
def test_wrong_file_types_fail_before_writing(tmp_path, relative):
    target = tmp_path / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if relative == "AGENTS.md":
        target.mkdir()
    else:
        target.write_text("This is a file")
    before = snapshot(tmp_path)
    with pytest.raises((InstallError, OSError)):
        install(tmp_path)
    assert snapshot(tmp_path) == before


@pytest.mark.parametrize("content", [START, END, END + START, START + START + END])
def test_malformed_agent_block_fails_without_changes(tmp_path, content):
    (tmp_path / "AGENTS.md").write_text(content)
    before = snapshot(tmp_path)
    with pytest.raises(InstallError, match="markers"):
        install(tmp_path)
    assert snapshot(tmp_path) == before


def test_update_requires_valid_installation(tmp_path):
    with pytest.raises(InstallError, match="not installed"):
        install(tmp_path, update=True)
    (tmp_path / ".agents").mkdir()
    (tmp_path / STATE).write_text('{"schema": 1, "files": "invalid"}')
    with pytest.raises(InstallError, match="Invalid installation"):
        install(tmp_path, update=True)


def test_cli_prompt_and_explicit_agent(tmp_path):
    runner = CliRunner()
    result = runner.invoke(app, ["init", "--path", str(tmp_path)], input="codex\n")
    assert result.exit_code == 0, result.output
    assert "Choose your agent" in result.output
    result = runner.invoke(app, ["init", "--path", str(tmp_path), "--agent", "codex"])
    assert result.exit_code == 0, result.output
    assert "Already up to date" in result.output
    result = runner.invoke(app, ["init", "--path", str(tmp_path), "--agent", "other"])
    assert result.exit_code == 2


def test_skill_manifests_and_relative_resources(tmp_path):
    install(tmp_path)
    for name in SKILLS:
        path = tmp_path / f".agents/skills/{name}/SKILL.md"
        frontmatter = yaml.safe_load(path.read_text().split("---", 2)[1])
        assert frontmatter["name"] == name
        assert frontmatter["description"]
    for name in SKILLS[1:]:
        folder = tmp_path / f".agents/skills/{name}"
        assert (folder / "../noggin/references/memory.md").is_file()
        assert (folder / "../noggin/templates/plan.md").is_file()
