import json
from dataclasses import dataclass


@dataclass
class DomainEvent:
    pass


@dataclass
class UserRegisteredEvent(DomainEvent):
    message: dict
    type: str = "UserRegisteredEvent"

    def to_json(self) -> str:
        return json.dumps({"type": self.type, "message": self.message})
