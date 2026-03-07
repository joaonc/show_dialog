from typing import Annotated

import typer

from admin.utils import DryAnnotation, run

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command(name='ruff')
def lint_ruff(
    path: Annotated[str, typer.Argument()] = '.',
    check: bool = False,
    dry: DryAnnotation = False,
):
    if check:
        run('ruff', 'check', path, dry=dry)
        run('ruff', 'format', '--check', path, dry=dry)
    else:
        run('ruff', 'check', '--fix', path, dry=dry)
        run('ruff', 'format', path, dry=dry)


@app.command(name='mypy')
def lint_mypy(path: Annotated[str, typer.Argument()] = '.', dry: DryAnnotation = False):
    run('mypy', path, dry=dry)


@app.command(name='all')
def lint_all(check: bool = False, dry: DryAnnotation = False):
    lint_ruff(path='.', check=check, dry=dry)
    lint_mypy(path='.', dry=dry)
