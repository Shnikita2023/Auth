import json
from dataclasses import dataclass


@dataclass
class DomainEvent:
    pass


@dataclass
class UserRegisteredEvent(DomainEvent):
    type: str
    message: dict

    def to_json(self) -> str:
        return json.dumps({"type": self.type, "message": self.message})
