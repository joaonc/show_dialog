import logging
import subprocess
from itertools import chain
from typing import Annotated

import typer

from admin import PROJECT_ROOT

DryAnnotation = Annotated[
    bool,
    typer.Option(
        help='Show the command that would be run without running it.',
        show_default=False,
    ),
]


def get_logger() -> logging.Logger:
    logger = logging.getLogger('typer-invoke')
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(handler)
    logger.propagate = False
    return logger


logger = get_logger()


def run(*args, dry: bool = False, **kwargs) -> subprocess.CompletedProcess | None:
    final_args = [str(arg) for arg in args if arg not in ['', None]]
    logger.info(' '.join(f'"{a}"' if (' ' in a) else a for a in final_args))

    if dry:
        return None

    defaults = dict(cwd=PROJECT_ROOT, capture_output=False, text=True, check=True)
    final_kwargs = defaults | kwargs
    try:
        return subprocess.run(final_args, **final_kwargs)  # type: ignore[arg-type]
    except subprocess.CalledProcessError as e:
        message = str(e)
        if e.stdout:
            message += f'\nSTDOUT:\n{e.stdout}'
        if e.stderr:
            message += f'\nSTDERR:\n{e.stderr}'
        logger.error(message)
        raise typer.Exit(1)


def multiple_parameters(parameter: str, *options) -> list[str]:
    return list(chain.from_iterable(zip([parameter] * len(options), map(str, options))))
