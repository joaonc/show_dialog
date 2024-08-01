from PySide6.QtCore import QDir, QFile, QTextStream


def list_resources(base_path: str = ':/', recursive: bool = False) -> list[str]:
    dir_ = QDir(base_path)

    files = []
    if recursive:
        dirs = dir_.entryList(QDir.Filter.Dirs)
        for subdir in dirs:
            files += list_resources(subdir, True)

    files = dir_.entryList(QDir.Filter.Files)

    return [f'{base_path}/{file}' for file in files]


def read_resource_file(file_path):
    file = QFile(file_path)
    if not file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        raise RuntimeError(f'Cannot open file: {file_path}')
    stream = QTextStream(file)
    content = stream.readAll()
    return content
