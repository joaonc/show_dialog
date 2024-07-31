import os
from pathlib import Path

from invoke import Collection, Exit, task

os.environ.setdefault('INVOKE_RUN_ECHO', '1')  # Show commands by default


PROJECT_ROOT = Path(__file__).parent
PROJECT_NAME = PROJECT_ROOT.name
ASSETS_DIR = PROJECT_ROOT / 'assets'
SOURCE_DIR = PROJECT_ROOT / 'src' / PROJECT_NAME

# Requirements files
REQUIREMENTS_MAIN = 'main'
REQUIREMENTS_FILES = {
    REQUIREMENTS_MAIN: 'requirements',
    'dev': 'requirements-dev',
    'docs': 'requirements-docs',
}
"""
Requirements files.
Order matters as most operations with multiple files need ``requirements.txt`` to be processed
first.
Add new requirements files here.
"""

REQUIREMENTS_TASK_HELP = {
    'requirements': '`.in` file. Full name not required, just the initial name after the dash '
    f'(ex. "dev"). For main file use "{REQUIREMENTS_MAIN}". Available requirements: '
    f'{", ".join(REQUIREMENTS_FILES)}.'
}

UI_FILES = tuple((ASSETS_DIR / 'ui').glob("**/*.ui"))
"""
QT ``.ui`` files.
"""

QRC_FILES = tuple(ASSETS_DIR.glob("**/*.qrc"))
"""
Qt ``.qrc`` resource files.
"""

# region Executable build configs
BUILD_SPEC_FILE = ASSETS_DIR / 'pyinstaller.spec'
BUILD_APP_MANIFEST_FILE = ASSETS_DIR / 'app.yaml'
BUILD_IN_FILE = SOURCE_DIR / 'main.py'
"""Executable input file."""
BUILD_WORK_DIR = PROJECT_ROOT / 'build'
BUILD_DIST_DIR = PROJECT_ROOT / 'dist'
# endregion


def _csstr_to_list(csstr: str) -> list[str]:
    """
    Convert a comma-separated string to list.
    """
    return [s.strip() for s in csstr.split(',')]


def _get_requirements_file(requirements: str, extension: str) -> str:
    """
    Return the full requirements file name (with extension).

    :param requirements: The requirements file to retrieve. Can be the whole filename
        (no extension), ex `'requirements-dev'` or just the initial portion, ex `'dev'`.
        Use `'main'` for the `requirements` file.
    :param extension: Requirements file extension. Can be either `'in'` or `'txt'`.
    """
    filename = REQUIREMENTS_FILES.get(requirements, requirements)
    if filename not in REQUIREMENTS_FILES.values():
        raise Exit(f'`{requirements}` is an unknown requirements file.')

    return f'{filename}.{extension.lstrip(".")}'


def _get_requirements_files(requirements: str | None, extension: str) -> list[str]:
    extension = extension.lstrip('.')
    if requirements is None:
        requirements_files = list(REQUIREMENTS_FILES)
    else:
        requirements_files = _csstr_to_list(requirements)

    # Get full filename+extension and sort by the order defined in `REQUIREMENTS_FILES`
    filenames = [
        _get_requirements_file(r, extension) for r in REQUIREMENTS_FILES if r in requirements_files
    ]

    return filenames


def _get_os_name():
    """User-friendly OS name (lowercased)."""
    import platform

    system = platform.system().lower()
    return {'darwin': 'mac'}.get(system, system)


def _get_build_files() -> tuple[Path, Path, Path]:
    import yaml

    manifest_file = BUILD_DIST_DIR / BUILD_APP_MANIFEST_FILE.name
    with open(BUILD_APP_MANIFEST_FILE) as f:
        manifest = yaml.safe_load(f)

    # Assumes the distribution directory is empty prior to creating the app
    files = [
        f
        for f in BUILD_DIST_DIR.glob('*')
        if f.is_file() and f != manifest_file and f.suffix.lower() != '.zip'
    ]
    if not files:
        raise Exit(f'App file not found in {BUILD_DIST_DIR}')
    if len(files) > 1:
        raise Exit(
            f'One file expected in the distribution folder {BUILD_DIST_DIR}.\n'
            f'{len(files)} files found:\n' + '\n'.join(str(file) for file in files)
        )
    app_file = files[0]
    zip_file = BUILD_DIST_DIR / f'{app_file.stem}_{manifest["version"]}_{_get_os_name()}.zip'

    return app_file, manifest_file, zip_file


def _check_git_tag_exists(tag) -> bool:
    import subprocess

    tags = subprocess.check_output(['git', 'tag', '--list'], text=True).split('\n')
    return tag in tags


def _get_git_commit() -> str:
    import subprocess

    return subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip().lower()


def _calculate_sha1(file_path):
    import hashlib

    # Initialize SHA1 hash object
    hasher = hashlib.sha1()

    with open(file_path, 'rb') as file:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: file.read(4096), b''):
            hasher.update(byte_block)

    return hasher.hexdigest()


@task
def build_clean(c):
    """
    Delete files created from previous builds (`build` and `dist` folders).
    """
    import shutil

    # From building the executable
    for d in [BUILD_WORK_DIR, BUILD_DIST_DIR]:
        shutil.rmtree(d, ignore_errors=True)

    # From building the package to publish in Pypi
    shutil.rmtree(PROJECT_ROOT / f'{PROJECT_NAME}.egg-info', ignore_errors=True)


@task(
    build_clean,
    help={
        'no_spec': f'Do not use the spec file `{BUILD_SPEC_FILE.relative_to(PROJECT_ROOT)}` and '
        f'create one in the `{BUILD_WORK_DIR.relative_to(PROJECT_ROOT)}` directory with defaults.',
        'no_zip': 'Do not create a ZIP file, which can be used to upload to a GitHub release.',
    },
)
def build_dist(c, no_spec: bool = False, no_zip: bool = False):
    """
    Build the distributable/executable file(s).
    """
    from datetime import datetime, timezone

    import yaml

    # Build executable
    if no_spec:
        c.run(
            f'pyinstaller '
            f'--onefile "{BUILD_IN_FILE}" --distpath "{BUILD_DIST_DIR}" '
            f'--workpath "{BUILD_WORK_DIR}" --specpath "{BUILD_WORK_DIR}"'
        )
    else:
        c.run(
            f'pyinstaller "{BUILD_SPEC_FILE}" '
            f'--distpath "{BUILD_DIST_DIR}" --workpath "{BUILD_WORK_DIR}"'
        )

    app_file, manifest_file, zip_file = _get_build_files()

    # App manifest file
    with open(BUILD_APP_MANIFEST_FILE) as f:
        manifest = yaml.safe_load(f)
    manifest |= {
        'build_time': datetime.now(timezone.utc),
        'git_commit': _get_git_commit(),
        'file_name': app_file.name,
        'file_sha1': _calculate_sha1(app_file),
    }

    with open(manifest_file, 'w') as f:
        f.write('# App manifest\n\n')
        yaml.safe_dump(manifest, f)

    # Zip file
    if no_zip:
        print('ZIP file not created.')
    else:
        import zipfile

        with zipfile.ZipFile(zip_file, 'w') as f:
            f.write(app_file, arcname=app_file.name)
            f.write(manifest_file, arcname=manifest_file.name)

    print('Done')


@task(
    help={
        'prerelease': 'Mark the release as a prerelease (beta).',
        'draft': 'Save the release as a draft instead of publishing it.',
        'no_upload': 'Do not upload artifacts to the release. Can be uploaded later with '
        '`inv build.upload`.',
        'notes': 'Release notes.',
        'notes_file': 'Read release notes from file. Ignores the `-notes` parameter.',
    },
)
def build_release(
    c,
    prerelease: bool = False,
    draft: bool = False,
    no_upload: bool = False,
    notes: str = '',
    notes_file: str = '',
):
    """
    Create a GitHub release with the current code.

    Need to be authenticated with `gh auth login` or by setting the `GH_TOKEN` environment variable
    with a GitHub API authentication token.
    """
    import shutil
    import zipfile

    import yaml

    if shutil.which('gh') is None:
        raise Exit(
            '`gh` command not found. '
            'Please install GitHub CLI (https://cli.github.com/) to proceed.'
        )

    if notes and notes_file:
        raise Exit('Both `--notes` and `--notes-file` are specified. Only one can be specified.')

    _, manifest_file, zip_file = _get_build_files()

    if not zip_file.exists():
        raise Exit(
            f'Zip file not found: {zip_file}\n'
            'Rebuild the app with `inv build.dist` and without the `--no-zip` option.'
        )

    # Get build info from manifest inside Zip
    with zipfile.ZipFile(zip_file) as f:
        manifest_str = f.read(manifest_file.name).decode()
    manifest = yaml.safe_load(manifest_str)

    # Prepare release
    app_version = manifest['version']
    release_tag = app_version
    release_title = f'v{app_version}' + (' (beta)' if prerelease else '')

    if _check_git_tag_exists(release_tag):
        raise Exit(
            f'Tag/Release `{release_tag}` already exists.\n'
            f'Update version in `{BUILD_APP_MANIFEST_FILE.relative_to(PROJECT_ROOT)}`.'
        )

    # Create release
    command = (
        f'gh release create "{release_tag}" "{zip_file}" --title "{release_title}" --generate-notes'
    )
    if notes:
        command += f' --notes "{notes}"'
    if notes_file:
        notes_file_path = Path(notes_file)
        command += f' --notes-file "{notes_file_path.resolve(strict=True)}"'
    if prerelease:
        command += ' --prerelease'
    if draft:
        command += ' --draft'

    c.run(command)


@task(
    help={
        'label': 'The label that will be displayed in GitHub next to the artifact. The special '
        'strings "auto" and "none" mean that the label is to be autogenerated (OS specific) or no '
        'label is attached, respectively. Any other string is what\'s used as label. Use the '
        '`--dry` option to see the label without uploading the artifact.'
    },
)
def build_upload(c, label: str = 'auto'):
    """
    Upload asset to the release in the manifest file.
    The artifact being uploaded is the Zip file with the executable binary for the current OS.
    The release the artifact is uploaded to is specified in the manifest file inside the Zip file.

    The following must already exist:
      * The artifact (`inv build.dist`).
      * The release in GitHub (`inv build.release`).
    """
    import zipfile

    import yaml

    _, manifest_file, zip_file = _get_build_files()

    if not zip_file.exists():
        raise Exit(
            f'Zip file not found: {zip_file}\n'
            'Rebuild the app with `inv build.dist` and without the `--no-zip` option.'
        )

    # Get build info from manifest inside Zip
    with zipfile.ZipFile(zip_file) as f:
        manifest_str = f.read(manifest_file.name).decode()
    manifest = yaml.safe_load(manifest_str)

    app_version = manifest['version']
    release_tag = app_version

    if not _check_git_tag_exists(release_tag):
        raise Exit(
            f'Tag/Release `{release_tag}` doesn\'t exist.\n'
            'Create release with `inv build.release` first.'
        )

    # Create label
    if label.lower() == 'auto':
        label = f'#{_get_os_name().title()}'
    elif label.lower() == 'none':
        label = ''
    else:
        label = f'#{label}'

    # Upload file
    command = f'gh release upload "{release_tag}" "{zip_file}{label}"'

    c.run(command)


@task(
    help={'no_upload': 'Do not upload to Pypi.'},
)
def build_publish(c, no_upload: bool = False):
    """
    Publish package to Pypi.
    """
    dist_dir = BUILD_DIST_DIR / 'package'
    # Create distribution files (source and wheel)
    # c.run(f'python setup.py sdist --dist-dir "{dist_dir}" bdist_wheel --dist-dir "{dist_dir}"')
    c.run(f'python -m build --outdir "{dist_dir}"')
    # Upload to pypi
    if not no_upload:
        c.run(f'twine upload "{dist_dir}/*"')


@task
def build_run(c):
    """
    Run the built package.
    """
    os_name = _get_os_name()

    if os_name == 'windows':
        exes = list(BUILD_DIST_DIR.glob('**/*.exe'))
        if len(exes) == 0:
            raise Exit('No executable found.')
        elif len(exes) > 1:
            raise Exit('Multiple executables found.')
        c.run(str(exes[0]))
    elif os_name == 'mac':
        app_file, _, _ = _get_build_files()
        c.run(str(app_file))
    elif os_name == 'linux':
        raise Exit('Running on Linux still needs to be implemented.')
    else:
        raise Exit(f'Running on {os_name.title()} is not supported.')


@task(
    help={
        'file': '`.ui` file to be converted to `.py`. `.ui` extension not required. '
        'Can be a comma separated list. If not supplied, all files will be converted. '
        f'Available files: {", ".join(p.stem for p in UI_FILES)}.'
    }
)
def ui_py(c, file=None):
    """
    Convert Qt `.ui` files into `.py`.
    """
    if file:
        file_stems = [
            (_f2[:-3] if _f2.lower().endswith('.ui') else _f2)
            for _f2 in [_f1.strip() for _f1 in file.split(',')]
        ]
    else:
        file_stems = [p.stem for p in UI_FILES]

    for file_stem in file_stems:
        try:
            file_path_in = next(p for p in UI_FILES if p.stem == file_stem)
        except StopIteration:
            raise Exit(
                f'File "{file}" not found. Available files: {", ".join(p.stem for p in UI_FILES)}'
            )

        file_path_out = SOURCE_DIR / 'ui/forms' / f'ui_{file_stem}.py'

        c.run(f'pyside6-uic {file_path_in} -o {file_path_out} --from-imports')


@task(
    help={
        'file': '`.qrc` file to be converted to `.py`. `.qrc` extension not required. '
        'Can be a coma separated list of filenames. If not supplied, all files will be converted. '
        f'Available files: {", ".join(p.stem for p in QRC_FILES)}.'
    }
)
def ui_rc(c, file=None):
    """
    Convert Qt `.qrc` files into `.py`.
    """
    if file:
        file_stems = [
            (_f2[:-4] if _f2.lower().endswith('.qrc') else _f2)
            for _f2 in [_f1.strip() for _f1 in file.split(',')]
        ]
    else:
        file_stems = [p.stem for p in QRC_FILES]

    for file_stem in file_stems:
        try:
            file_path_in = next(p for p in QRC_FILES if p.stem == file_stem)
        except StopIteration:
            raise Exit(
                f'File "{file}" not found. Available files: {", ".join(p.stem for p in QRC_FILES)}'
            )

        file_path_out = SOURCE_DIR / 'ui/forms' / f'{file_stem}_rc.py'

        c.run(f'pyside6-rcc {file_path_in} -o {file_path_out}')


@task(
    help={
        'file': f'`.ui` file to be edited. Available files: {", ".join(p.stem for p in UI_FILES)}.'
    }
)
def ui_edit(c, file):
    """
    Edit a file in QT Designer.
    """
    file_stem = file[:-3] if file.lower().endswith('.ui') else file
    try:
        ui_file_path = next(p for p in UI_FILES if p.stem == file_stem)
    except StopIteration:
        raise Exit(
            f'File "{file}" not found. Available files: {", ".join(p.stem for p in UI_FILES)}'
        )

    c.run(f'pyside6-designer {ui_file_path}', asynchronous=True)


@task
def lint_black(c, path='.'):
    c.run(f'black {path}')


@task
def lint_flake8(c, path='.'):
    c.run(f'flake8 {path}')


@task
def lint_isort(c, path='.'):
    c.run(f'isort {path}')


@task
def lint_mypy(c, path='.'):
    c.run(f'mypy {path}')


@task(lint_isort, lint_black, lint_flake8, lint_mypy)
def lint_all(c):
    """
    Run all linters.
    Config for each of the tools is in ``pyproject.toml`` and ``setup.cfg``.
    """
    print('Done')


@task
def test_unit(c):
    """
    Run unit tests.
    """
    c.run('python -m pytest')


@task(help=REQUIREMENTS_TASK_HELP)
def pip_compile(c, requirements=None):
    """
    Compile requirements file(s).
    """
    for filename in _get_requirements_files(requirements, 'in'):
        c.run(f'pip-compile {filename}')


@task(help=REQUIREMENTS_TASK_HELP)
def pip_sync(c, requirements=None):
    """
    Synchronize environment with requirements file.
    """
    c.run(f'pip-sync {" ".join(_get_requirements_files(requirements, "txt"))}')


@task(
    help=REQUIREMENTS_TASK_HELP | {'package': 'Package to upgrade. Can be a comma separated list.'}
)
def pip_package(c, requirements, package):
    """
    Upgrade package.
    """
    packages = [p.strip() for p in package.split(',')]
    for filename in _get_requirements_files(requirements, 'in'):
        c.run(f'pip-compile --upgrade-package {" --upgrade-package ".join(packages)} {filename}')


@task(help=REQUIREMENTS_TASK_HELP)
def pip_upgrade(c, requirements):
    """
    Try to upgrade all dependencies to their latest versions.
    """
    for filename in _get_requirements_files(requirements, 'in'):
        c.run(f'pip-compile --upgrade {filename}')


@task
def precommit_install(c):
    """
    Install pre-commit into the git hooks, which will cause pre-commit to run on automatically.
    This should be the first thing to do after cloning this project and installing requirements.
    """
    c.run('pre-commit install')


@task
# `upgrade` instead of `update` to maintain similar naming to `pip-compile upgrade`
def precommit_upgrade(c):
    """
    Upgrade pre-commit config to the latest repos' versions.
    """
    c.run('pre-commit autoupdate')


@task(help={'hook': 'Name of hook to run. Default is to run all.'})
def precommit_run(c, hook=None):
    """
    Manually run pre-commit hooks.
    """
    hook = hook or '--all-files'
    c.run(f'pre-commit run {hook}')


@task
def docs_serve(c):
    """
    Start documentation local server.
    """
    c.run('mkdocs serve')


@task
def docs_deploy(c):
    """
    Publish documentation to GitHub Pages at https://joaonc.github.io/show_dialog
    """
    c.run('mkdocs gh-deploy')


@task
def docs_clean(c):
    """
    Delete documentation website static files.
    """
    import shutil

    shutil.rmtree(PROJECT_ROOT / 'site', ignore_errors=True)


ns = Collection()  # Main namespace

test_collection = Collection('test')
test_collection.add_task(test_unit, 'unit')

build_collection = Collection('build')
build_collection.add_task(build_clean, 'clean')
build_collection.add_task(build_dist, 'dist')
build_collection.add_task(build_release, 'release')
build_collection.add_task(build_run, 'run')
build_collection.add_task(build_upload, 'upload')
build_collection.add_task(build_publish, 'publish')

lint_collection = Collection('lint')
lint_collection.add_task(lint_all, 'all')
lint_collection.add_task(lint_black, 'black')
lint_collection.add_task(lint_flake8, 'flake8')
lint_collection.add_task(lint_isort, 'isort')
lint_collection.add_task(lint_mypy, 'mypy')

pip_collection = Collection('pip')
pip_collection.add_task(pip_compile, 'compile')
pip_collection.add_task(pip_package, 'package')
pip_collection.add_task(pip_sync, 'sync')
pip_collection.add_task(pip_upgrade, 'upgrade')

precommit_collection = Collection('precommit')
precommit_collection.add_task(precommit_run, 'run')
precommit_collection.add_task(precommit_install, 'install')
precommit_collection.add_task(precommit_upgrade, 'upgrade')

docs_collection = Collection('docs')
docs_collection.add_task(docs_serve, 'serve')
docs_collection.add_task(docs_deploy, 'deploy')
docs_collection.add_task(docs_clean, 'clean')

ui_collection = Collection('ui')
ui_collection.add_task(ui_py, 'py')
ui_collection.add_task(ui_rc, 'rc')
ui_collection.add_task(ui_edit, 'edit')

ns.add_collection(build_collection)
ns.add_collection(lint_collection)
ns.add_collection(pip_collection)
ns.add_collection(precommit_collection)
ns.add_collection(test_collection)
ns.add_collection(docs_collection)
ns.add_collection(ui_collection)
