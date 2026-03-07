from enum import Enum
from pathlib import Path
from typing import Annotated

import typer

from admin import PROJECT_ROOT
from admin.utils import DryAnnotation, logger, multiple_parameters, run

REQUIREMENTS_DIR = PROJECT_ROOT / 'admin' / 'requirements'

app = typer.Typer(no_args_is_help=True, add_completion=False)


class Requirements(str, Enum):
    MAIN = 'requirements'
    DEV = 'requirements-dev'
    DOCS = 'requirements-docs'


class RequirementsType(str, Enum):
    IN = 'in'
    OUT = 'txt'


RequirementsAnnotation = Annotated[
    list[str] | None,
    typer.Argument(
        help='Requirement file(s). If not set, all files are used.',
        show_default=False,
    ),
]


def _get_requirements_file(
    requirements: str | Requirements, requirements_type: str | RequirementsType
) -> Path:
    if isinstance(requirements, Requirements):
        reqs = requirements
    else:
        try:
            reqs = Requirements(requirements.lower())
        except ValueError:
            logger.error(f'`{requirements}` is an unknown requirements file.')
            raise typer.Exit(1)

    reqs_type = (
        requirements_type
        if isinstance(requirements_type, RequirementsType)
        else RequirementsType(requirements_type.lstrip('.').lower())
    )
    return REQUIREMENTS_DIR / f'{reqs.value}.{reqs_type.value}'


def _get_requirements_files(
    requirements: list[str | Requirements] | None, requirements_type: str | RequirementsType
) -> list[Path]:
    requirements_files = list(Requirements) if requirements is None else requirements
    return [_get_requirements_file(r, requirements_type) for r in requirements_files]


@app.command(name='compile')
def pip_compile(
    requirements: RequirementsAnnotation = None, clean: bool = False, dry: DryAnnotation = False
):
    if clean and not dry:
        for filename in _get_requirements_files(requirements, RequirementsType.OUT):
            filename.unlink(missing_ok=True)

    for filename in _get_requirements_files(requirements, RequirementsType.IN):
        output_file = filename.with_suffix('.txt')
        run(
            'uv',
            'pip',
            'compile',
            '--no-header',
            '--no-strip-extras',
            filename.name,
            '-o',
            output_file.name,
            dry=dry,
            cwd=REQUIREMENTS_DIR,
        )


@app.command(name='sync')
def pip_sync(requirements: RequirementsAnnotation = None, dry: DryAnnotation = False):
    run('uv', 'pip', 'sync', *_get_requirements_files(requirements, RequirementsType.OUT), dry=dry)


@app.command(name='package')
def pip_package(
    requirements: RequirementsAnnotation,
    package: Annotated[list[str], typer.Option('--package', '-p')],
    dry: DryAnnotation = False,
):
    for filename in _get_requirements_files(requirements, RequirementsType.IN):
        output_file = filename.with_suffix('.txt')
        run(
            'uv',
            'pip',
            'compile',
            *multiple_parameters('--upgrade-package', *package),
            str(filename),
            '-o',
            str(output_file),
            dry=dry,
        )


@app.command(name='upgrade')
def pip_upgrade(requirements: RequirementsAnnotation = None, dry: DryAnnotation = False):
    for filename in _get_requirements_files(requirements, RequirementsType.IN):
        output_file = filename.with_suffix('.txt')
        run(
            'uv',
            'pip',
            'compile',
            '--no-strip-extras',
            '--upgrade',
            str(filename),
            '-o',
            str(output_file),
            dry=dry,
        )


@app.command(name='install')
def pip_install(requirements: RequirementsAnnotation = None, dry: DryAnnotation = False):
    requirements_files = _get_requirements_files(requirements, RequirementsType.OUT)
    run('uv', 'pip', 'install', *multiple_parameters('-r', *requirements_files), dry=dry)
