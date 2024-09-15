from dataclasses import dataclass

from ..data_class import DefaultsMixin, JSONFileMixin

@dataclass
class IpcParams(JSONFileMixin, DefaultsMixin):
    """
    Inter-Process Communication parameters.
    """

    host: str
    port: int
    timeout: int
