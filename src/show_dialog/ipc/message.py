import json
from dataclasses import dataclass, asdict, field
from enum import Enum


class MessageType(str, Enum):
    MESSAGE = 'message'
    TIMEOUT = 'timeout'
    ACK = 'ack'
    PASS = 'pass'
    FAIL = 'fail'


@dataclass
class Message:
    type: str | MessageType
    message: str = ''
    data: dict = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.type, str):
            self.type = MessageType(self.type)

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> 'Message':
        obj_dict = json.loads(json_str)
        return cls(**obj_dict)
