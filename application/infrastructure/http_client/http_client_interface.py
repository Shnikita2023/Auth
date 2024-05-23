import json
from abc import abstractmethod, ABC
from typing import Optional


class HTTPClientInterface(ABC):
    @abstractmethod
    async def get(self, url: str) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    async def post(self, url: str, data: json) -> Optional[str]:
        raise NotImplementedError
