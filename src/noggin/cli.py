from pathlib import Path
from typing import Annotated

import typer

from noggin import __version__
from noggin.installer import InstallError, install

app = typer.Typer(no_args_is_help=True, help="A little memory for coding agents.")
Project = Annotated[Path, typer.Option("--path", "-p", help="Project directory.")]


def run_install(path: Path, *, update: bool = False) -> None:
    try:
        changed = install(path, update=update)
    except (InstallError, OSError, UnicodeError) as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(1) from exc
    typer.echo(f"{'Updated' if update else 'Initialized'} noggin in {path.resolve()}")
    typer.echo(f"{len(changed)} files written." if changed else "Already up to date.")


@app.command()
def init(
    path: Project = Path("."),
    agent: Annotated[str | None, typer.Option(help="Agent to install for.")] = None,
) -> None:
    """Create memory and install project-local skills without replacing files."""
    if agent is None:
        agent = typer.prompt("Choose your agent (codex)", default="codex")
    if agent.lower() != "codex":
        typer.echo("Only codex is supported in this version.", err=True)
        raise typer.Exit(2)
    run_install(path)


@app.command()
def update(path: Project = Path(".")) -> None:
    """Refresh unmodified installed skills; preserve memory and local edits."""
    run_install(path, update=True)


@app.command()
def version() -> None:
    """Print the installed version."""
    typer.echo(__version__)
