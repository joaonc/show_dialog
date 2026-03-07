from pathlib import Path
from typing import Annotated

import typer

from admin import PROJECT_ROOT, SOURCE_DIR
from admin.utils import DryAnnotation, logger, run

app = typer.Typer()

BUILD_DIST_DIR = PROJECT_ROOT / 'dist'
BUILD_WORK_DIR = PROJECT_ROOT / 'build'
BUILD_DIST_APP_DIR = BUILD_DIST_DIR / 'app'
BUILD_WORK_APP_DIR = BUILD_WORK_DIR / 'app'
BUILD_SPEC_FILE = PROJECT_ROOT / 'assets' / 'pyinstaller.spec'
VERSION_FILES = [PROJECT_ROOT / 'pyproject.toml', SOURCE_DIR / 'show_dialog' / '__init__.py']


@app.command()
def clean():
    import shutil

    shutil.rmtree(BUILD_DIST_DIR, ignore_errors=True)


def _get_project_version() -> str:
    import re

    pattern = re.compile("""^[ _]*version[ _]*[:=] *['"](.*)['"]""", re.MULTILINE)
    versions = {}
    for file in VERSION_FILES:
        with open(file) as f:
            text = f.read()
        match = pattern.search(text)
        if not match:
            logger.error(f'Could not find version in `{file.relative_to(PROJECT_ROOT)}`.')
            raise typer.Exit(1)
        versions[file] = match.group(1)

    if len(set(versions.values())) != 1:
        logger.error('Version mismatch in files that contain versions.')
        raise typer.Exit(1)

    return list(versions.values())[0]


def _re_sub_file(file: str | Path, regex: str, repl: str, save: bool = True) -> str:
    import re

    pattern = re.compile(regex, re.MULTILINE)
    with open(file) as f:
        text = f.read()
    new_text = pattern.sub(lambda match: f'{match.group(1)}{repl}{match.group(3)}', text)

    if save:
        with open(file, 'w') as f:
            f.write(new_text)

    return new_text


def _update_project_version(version: str):
    regex = r"""^([ _]*version[ _]*[:=] *['"])(.*)(['"].*)$"""
    for file in VERSION_FILES:
        _re_sub_file(file, regex, version)


def _get_next_version(current_version: str, part: str) -> str:
    from packaging.version import Version

    version = Version(str(current_version))
    if part == 'major':
        new_version = Version(f'{version.major + 1}.0.0')
    elif part == 'minor':
        new_version = Version(f'{version.major}.{version.minor + 1}.0')
    elif part == 'patch':
        new_version = Version(f'{version.major}.{version.minor}.{version.micro + 1}')
    else:
        raise ValueError('`part` must be "major", "minor", or "patch"')
    return str(new_version)


@app.command(name='version')
def version_set(
    version: Annotated[str, typer.Option()] = '',
    bump: Annotated[str, typer.Option()] = '',
    mode: Annotated[str, typer.Option()] = 'nothing',
    yes: Annotated[bool, typer.Option()] = False,
    dry: DryAnnotation = False,
):
    if version and bump:
        logger.error('Either `version` or `bump` can be set, not both.')
        raise typer.Exit(1)
    current_version = _get_project_version()
    new_version = version or _get_next_version(current_version, bump.strip().lower() or 'patch')
    _update_project_version(new_version)
    logger.info(f'Updated version from `{current_version}` to `{new_version}`.')
    if mode in ['commit', 'pr']:
        run('git', 'add', *VERSION_FILES, dry=dry)
        run('git', 'commit', '-m', f'bump version to {new_version}', dry=dry)
        branch = run('git', 'branch', '--show-current', dry=dry, capture_output=True)
        if branch:
            run('git', 'push', 'origin', branch.stdout.strip(), dry=dry)
    if mode == 'pr':
        run(
            'gh',
            'pr',
            'create',
            '--title',
            f'Release {new_version}',
            '--body',
            f'Preparing for release {new_version}',
            dry=dry,
        )
        run('gh', 'pr', 'merge', '--squash', '--auto', dry=dry)
    _ = yes


@app.command(name='publish')
def publish(
    upload: Annotated[bool, typer.Option(help='Upload to PyPI after build.')] = True,
    yes: Annotated[bool, typer.Option(help='Skip publish confirmation.')] = False,
    dry: DryAnnotation = False,
):
    run('uv', 'build', dry=dry)
    if not upload:
        return

    msg = f'Publishing version `{_get_project_version()}` to PyPI. Press Y to confirm. '
    if yes or input(msg).strip().lower() == 'y':
        run('uv', 'publish', dry=dry)
    else:
        logger.info('Package not published to PyPI.')


@app.command(name='release')
def release(
    notes: Annotated[str, typer.Option()] = '',
    notes_file: Annotated[str, typer.Option()] = '',
    yes: Annotated[bool, typer.Option()] = False,
    dry: DryAnnotation = False,
):
    if notes and notes_file:
        logger.error('Both `--notes` and `--notes-file` are specified. Use only one.')
        raise typer.Exit(1)
    version = _get_project_version()
    tag = version
    release_name = f'v{version}'
    args = ['gh', 'release', 'create', tag, '--title', release_name, '--generate-notes']
    if notes:
        args.extend(['--notes', notes])
    if notes_file:
        args.extend(['--notes-file', notes_file])
    msg = f'Creating GitHub release `{release_name}`. Press Y to confirm. '
    if yes or input(msg).strip().lower() == 'y':
        run(*args, dry=dry)


@app.command(name='app')
def build_app(dry: DryAnnotation = False):
    run(
        'pyinstaller',
        str(BUILD_SPEC_FILE),
        '--distpath',
        str(BUILD_DIST_APP_DIR),
        '--workpath',
        str(BUILD_WORK_APP_DIR),
        dry=dry,
    )


@app.command(name='upload')
def upload(dry: DryAnnotation = False):
    zip_files = sorted(BUILD_DIST_APP_DIR.glob('*.zip'))
    if not zip_files:
        logger.error(f'No .zip file found in `{BUILD_DIST_APP_DIR}`.')
        raise typer.Exit(1)
    latest_zip = zip_files[-1]
    version = _get_project_version()
    run('gh', 'release', 'upload', version, str(latest_zip), dry=dry)


if __name__ == '__main__':
    app()
