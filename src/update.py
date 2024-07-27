import logging
import shutil
import sys
from datetime import datetime
from pathlib import Path

from semantic_version import Version

import src.config as config


class FileUpdateError(Exception): ...


def check_update(update_manifest=None) -> tuple[bool, Version | None]:
    """
    Check if there's a newer version of the app.

    :param update_manifest: The new app's  manifest file location.

    :returns: Tuple with boolean on whether the app needs to be updated and the version it was
    compared to. This version is the update version if the ``True`` and it's ``None`` if there's
    no manifest file for the update.

    :raises FileNotFoundError: If the update manifest file doesn't exist.
    """
    update_manifest = update_manifest or config.update_manifest

    if not update_manifest:
        return False, None

    update_manifest_dict = config.read_manifest_file(update_manifest)
    new_app_version = Version(update_manifest_dict['version'])

    return config.version < new_app_version, new_app_version


def perform_update(update_file=None):
    """

    The file can't be updated with a simple copy because the app is running, thus locking the file.

    The key is that the file *can* be renamed (even while locked) and then a new file can be copied/
    moved in its place. On the next app start, it will be running the new version.

    1. Rename currently running file (to ``.bak``).
    2. Copy new version to where the currently running version is (before the rename).
    3. Re-launch the app.

    :param update_file: File to update to.

    :raises EnvironmentError: Running as a Python script. Code needs to be running as executable
        bundled with PyInstaller.
    :raises FileNotFoundError: Update file not found.
    :raises FileUpdateError: Error on update and rolled back. Info on the underlying error included.
    :raises ValueError: Update file not specified either in the parameter of this function or in
        the ``config`` module.
    """
    if not config.IS_BUNDLED_APP and not config.IGNORE_BUNDLED_APP:
        raise EnvironmentError('Update only works when running the bundled (executable) app.')

    update_file = update_file or config.update_file
    if not update_file:
        raise ValueError('Update file not set.')
    if not (update_file := Path(update_file)).exists():
        raise FileNotFoundError(f'Update file not found: {update_file}')

    current_file = Path(sys.executable).resolve()
    logging.debug(f'Updating file {current_file}')

    # Rename currently running app
    backup_file_path = (
        current_file.parent / f'{current_file.stem}.bak_{int(datetime.now().timestamp())}'
    )
    logging.debug(f'Backing up file to {backup_file_path}')
    if not config.IGNORE_UPDATE:
        backup_file = current_file.rename(backup_file_path)
        config.backup_file = backup_file
    else:
        logging.debug('Not backing up file due to `SHOW_DIALOG_IGNORE_UPDATE` being set.')

    # Substitute with new file
    try:
        logging.debug(f'Copying new version from {update_file}')
        if not config.IGNORE_UPDATE:
            shutil.copy(update_file, current_file)
        else:
            logging.debug('Not copying file due to `SHOW_DIALOG_IGNORE_UPDATE` being set.')
    except Exception as e:
        logging.debug('Update failed, rolling back.')
        backup_file.rename(current_file)  # noqa
        raise FileUpdateError('Error updating executable file. Rolled back.') from e
