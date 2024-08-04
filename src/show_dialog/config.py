"""
Global configs.

Uppercase denotes global constants that should not be parametrized (ie, changed on different runs).
"""

import os
import sys
from pathlib import Path

import yaml
from packaging.version import Version


def read_manifest_file(manifest) -> dict:
    with open(manifest) as f:
        return yaml.safe_load(f)  # type: ignore


def is_truthy(value) -> bool:
    return str(value).strip().lower() in ['true', '1']


# region Run configs
IS_BUNDLED_APP = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
"""
Whether the code is running as an executable bundled by PyInstaller or as normal Python code.

More info at https://pyinstaller.org/en/stable/runtime-information.html
"""

IGNORE_BUNDLED_APP = is_truthy(os.environ.get('SHOW_DIALOG_IGNORE_BUNDLED_APP', 'False'))
"""
Ignore ``IS_BUNDLED_APP``, ie, code that is supposed to execute only as a bundled app will run as
script also.

To be used for debugging purposes.

Set the environment variable ``SHOW_DIALOG_IGNORE_BUNDLED_APP`` to ``True`` or ``1`` when
executing the code as a script. Ignored when running as a bundled app.
"""

if IS_BUNDLED_APP:
    PROJECT_ROOT = Path(sys._MEIPASS)  # type: ignore
else:
    PROJECT_ROOT = Path(__file__).parents[2]

ASSETS_DIR = PROJECT_ROOT / 'assets'
APP_MANIFEST_FILE = ASSETS_DIR / 'app.yaml'
# endregion

# region Global constants
ORGANIZATION_NAME = 'Show Dialog'
ORGANIZATION_DOMAIN = 'show-dialog.app'
APPLICATION_NAME = 'Show Dialog'
# endregion

# region General configs
app_manifest = read_manifest_file(APP_MANIFEST_FILE)
"""
App manifest contents (as a dict).
"""

version = Version(app_manifest['version'])
"""App version."""
# endregion
