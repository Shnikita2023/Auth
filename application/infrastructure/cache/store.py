""" Абстрактный репозиторий для хранения данных ключ-значение """

from abc import abstractmethod, ABC


class CacheStore(ABC):
    @abstractmethod
    async def connect(self):
        raise NotImplementedError

    @abstractmethod
    async def get(self, key):
        raise NotImplementedError

    @abstractmethod
    async def get_multi(self, *keys):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key):
        raise NotImplementedError

    @abstractmethod
    async def delete_multi(self, *keys):
        raise NotImplementedError

    @abstractmethod
    async def set(self, key, value):
        raise NotImplementedError

    @abstractmethod
    async def set_multi(self, **key_vals):
        raise NotImplementedError

    @abstractmethod
    async def search(self, match):
        raise NotImplementedError

    @abstractmethod
    async def shutdown(self):
        raise NotImplementedError


async def get_cache_client():
    raise NotImplementedError
