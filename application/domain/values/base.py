from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any

VT = TypeVar("VT", bound=Any)


@dataclass(frozen=True)
class BaseValueObjects(ABC, Generic[VT]):
    value: VT

    def __post_init__(self):
        self.validate()

    @abstractmethod
    def validate(self) -> None:
        raise NotImplemented
