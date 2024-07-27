import json
from typing import Type, TypeVar

from dataclasses import dataclass
from pathlib import Path

from mashumaro.mixins.json import DataClassJSONMixin

T = TypeVar('T', bound='JSONFileMixin')


class JSONFileMixin(DataClassJSONMixin):
    def to_file(self, file: str | Path):
        file_path = Path(file)
        data = self.to_json()
        with open(file_path, 'w') as f:
            f.write(data)

    @classmethod
    def from_file(cls: Type[T], file: str | Path) -> T:
        file_path = Path(file)
        with open(file_path) as f:
            data = f.read()
        return cls.from_json(T, data)


@dataclass
class Inputs(JSONFileMixin):
    """
    Inputs to the app.
    """

    title: str
    description: str
