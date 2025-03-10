from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from application.config import settings
from application.infrastructure.db.database import async_session_maker
from application.repos.models import Base
from application.web.app import main_app

DATABASE_URL_TEST: str = settings.db.database_test_url_asyncpg

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker_test: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture()
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker_test() as session:
        yield session


main_app.dependency_overrides[async_session_maker] = async_session_maker_test
main_app.dependency_overrides[async_session_maker_test] = async_session


@pytest.fixture(autouse=True)
async def prepare_database():
    """Фикстура на создание и удаление таблицы"""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture()
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Фикстура для создания асинхронного клиента"""
    async with AsyncClient(transport=ASGITransport(app=main_app), base_url="http://test") as async_client:
        yield async_client
