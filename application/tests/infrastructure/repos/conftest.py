from sqlalchemy.ext.asyncio import AsyncSession

from application.repos.credential import SQLAlchemyCredentialRepository


def repo(async_session: AsyncSession) -> SQLAlchemyCredentialRepository:
    return SQLAlchemyCredentialRepository(session=async_session)