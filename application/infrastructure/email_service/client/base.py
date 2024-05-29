from abc import ABC, abstractmethod

from pydantic import EmailStr


class EmailClient(ABC):

    @abstractmethod
    async def connect(self):
        raise NotImplementedError

    @abstractmethod
    async def disconnect(self):
        raise NotImplementedError

    @abstractmethod
    async def send_notification(self, body: str, email: EmailStr, title: str):
        raise NotImplementedError
