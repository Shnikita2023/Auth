from abc import ABC, abstractmethod


class Producer(ABC):
    @abstractmethod
    async def initialization(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delivery_message(self, message: str, topic: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def finalization(self) -> None:
        raise NotImplementedError
