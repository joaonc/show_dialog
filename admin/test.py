import typer

from admin.utils import DryAnnotation, run

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command(name='unit')
def test_unit(dry: DryAnnotation = False):
    run('python', '-m', 'pytest', dry=dry)
