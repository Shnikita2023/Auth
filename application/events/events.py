import json
from dataclasses import dataclass


@dataclass
class DomainEvent:
    message: dict
    type: str

    def to_json(self) -> str:
        created_at = self.message.get("created_at")
        self.message["created_at"] = created_at.strftime('%Y-%m-%d %H:%M:%S')
        return json.dumps({"type": self.type, "message": self.message}, ensure_ascii=False)


@dataclass
class UserRegisteredEvent(DomainEvent):
    type: str = "UserRegisteredEvent"


@dataclass
class UserUpdatedStatusEvent(DomainEvent):
    type: str = "UserUpdatedStatusEvent"
