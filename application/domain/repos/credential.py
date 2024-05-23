from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from application.domain.entities.credential import Credential as DomainCredential


class AbstractCredentialRepository(ABC):

    @abstractmethod
    async def add(self, session: AsyncSession, user: DomainCredential) -> DomainCredential:
        raise NotImplemented

    @abstractmethod
    async def get_user_by_param(self, session: AsyncSession, params: dict[str, Any]) -> DomainCredential | None:
        raise NotImplemented
