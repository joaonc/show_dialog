"""
Run tests with pytest.
"""

import typer

from admin.utils import DryAnnotation, run

app = typer.Typer(
    help=__doc__,
    no_args_is_help=True,
    add_completion=False,
    rich_markup_mode='markdown',
)


@app.command(name='unit')
def test_unit(dry: DryAnnotation = False):
    run('python', '-m', 'pytest', dry=dry)


if __name__ == '__main__':
    app()
