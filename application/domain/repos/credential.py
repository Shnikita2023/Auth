from abc import ABC, abstractmethod
from typing import Optional, Any

from application.domain.entities.credential import Credential as DomainCredential


class AbstractCredentialRepository(ABC):

    @abstractmethod
    async def add(self, user: DomainCredential) -> DomainCredential:
        raise NotImplemented

    @abstractmethod
    async def get(self, user_oid: str) -> DomainCredential | None:
        raise NotImplemented

    @abstractmethod
    async def get_one_by_any_params(self, params: dict[str, Any]) -> Optional[DomainCredential]:
        raise NotImplemented

    @abstractmethod
    async def get_one_by_all_params(self, params: dict[str, Any]) -> Optional[DomainCredential]:
        raise NotImplemented

