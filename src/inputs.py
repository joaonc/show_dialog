import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Type, TypeVar

from mashumaro.mixins.json import DataClassJSONMixin

T = TypeVar('T', bound='JSONFileMixin')


class JSONFileMixin(DataClassJSONMixin):
    def to_file(self, file: str | Path, **from_dict_kwargs: Any):
        file_path = Path(file)
        data = self.to_dict(**from_dict_kwargs)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    @classmethod
    def from_file(cls: Type[T], file: str | Path, **from_dict_kwargs: Any) -> T:
        file_path = Path(file)
        with open(file_path) as f:
            data = json.load(f)
        return cls.from_dict(data, **from_dict_kwargs)


@dataclass
class Inputs(JSONFileMixin):
    """
    Inputs to the app.
    """

    title: str
    description: str
