from typing import Any

from sqlalchemy import select, Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from application.domain.entities.credential import Credential as DomainCredential
from application.domain.repos.credential import AbstractCredentialRepository
from application.exceptions import DBError
from application.repos.models import Credential


class SQLAlchemyCredentialRepository(AbstractCredentialRepository):
    """
    Класс для работы с базой данных пользователя
    """

    @classmethod
    async def add(cls, session: AsyncSession, credo: DomainCredential) -> DomainCredential:
        try:
            model: Credential = Credential.from_entity(credo)
            session.add(model)
            await session.commit()
            return credo

        except SQLAlchemyError as exc:
            raise DBError(exc)

    #
    # @classmethod
    # async def get_user_by_field(cls, session: AsyncSession, column: str, value: Any):
    #     try:
    #         query = select(User).filter_by(**{column: value})
    #         result: Result = await session.execute(query)
    #         user: User | None = result.scalar_one_or_none()
    #         return user
    #
    #     except ConnectionError:
    #         raise HttpAPIException(exception=cls.error_bd).http_error_500

    @classmethod
    async def get_user_by_param(cls, session: AsyncSession, params: dict[str, Any]) -> DomainCredential | None:
        try:
            query = select(Credential).filter_by(**params)
            result: Result = await session.execute(query)
            user: Credential | None = result.scalar_one_or_none()
            if user:
                return user.to_entity()

        except SQLAlchemyError as exc:
            raise DBError(exc)

    # @classmethod
    # async def get_user_by_id(cls, session: AsyncSession, user_id: int) -> User | None:
    #     try:
    #         user: User | None = await session.get(User, user_id)
    #         return user
    #
    #     except ConnectionError:
    #         raise HttpAPIException(exception=cls.error_bd).http_error_500

    # @classmethod
    # async def get_emails_users(cls, session: AsyncSession) -> list:
    #     try:
    #         query = select(User.email)
    #         result: Result = await session.execute(query)
    #         emails_users = result.scalars().all()
    #         return list(emails_users)
    #
    #     except ConnectionError:
    #         raise HttpAPIException(exception=cls.error_bd).http_error_500
    #
    # @classmethod
    # async def update_partially_data_user(cls,
    #                                      session: AsyncSession,
    #                                      id_data: int,
    #                                      new_data: Any):
    #     try:
    #         stmt = update(User).where(User.id == id_data).values(new_data)
    #         await session.execute(stmt)
    #         await session.commit()
    #         return new_data
    #
    #     except ConnectionError:
    #         raise HttpAPIException(exception=cls.error_bd).http_error_500
    #


credential_db = SQLAlchemyCredentialRepository()
