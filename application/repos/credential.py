from typing import Any, Optional

from sqlalchemy import select, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from application.domain.entities.credential import Credential as DomainCredential
from application.domain.repos.credential import AbstractCredentialRepository
from application.exceptions import DBError
from application.repos.models import Credential


class SQLAlchemyCredentialRepository(AbstractCredentialRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, credo: DomainCredential) -> DomainCredential:
        try:
            credo_model: Credential = Credential.from_entity(credo)
            self.session.add(credo_model)
            return credo

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def get(self, credo_oid: str) -> DomainCredential | None:
        try:
            query = select(Credential).where(Credential.oid == credo_oid)
            result = await self.session.execute(query)
            credo_model: Optional[Credential] = result.scalar_one_or_none()
            if credo_model:
                return credo_model.to_entity()

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def get_one_by_any_params(self, params: dict[str, Any]) -> Optional[DomainCredential]:
        try:
            filters = [getattr(Credential, field) == value for field, value in params.items()]
            query = select(Credential).where(or_(*filters))
            result = await self.session.execute(query)
            credo_model: Optional[Credential] = result.scalar_one_or_none()
            if credo_model:
                return credo_model.to_entity()

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def get_one_by_all_params(self, params: dict[str, Any]) -> Optional[DomainCredential]:
        try:
            query = select(Credential).filter_by(**params)
            result = await self.session.execute(query)
            credo_model: Optional[Credential] = result.scalar_one_or_none()
            if credo_model:
                return credo_model.to_entity()

        except SQLAlchemyError as exc:
            raise DBError(exc)




