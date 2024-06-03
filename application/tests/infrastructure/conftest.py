import pytest

from application.domain.values.credential import FullName, Email, Password, Phone
from application.repos.credential import SQLAlchemyCredentialRepository
from application.tests.conftest import async_session_maker_test
from application.domain.entities.credential import Credential as DomainCredential


@pytest.fixture
async def repo() -> SQLAlchemyCredentialRepository:
    async with async_session_maker_test() as session:
        yield SQLAlchemyCredentialRepository(session=session)


@pytest.fixture()
async def credential() -> DomainCredential:
    return DomainCredential(
        oid="4aca4d42-d7cf-44dc-9081-4de782d465ff",
        first_name=FullName("Alice"),
        last_name=FullName("Smith"),
        middle_name=FullName("Middle"),
        email=Email("alice@example.com"),
        password=Password("Password!123"),
        time_call="in 8h",
        number_phone=Phone("89031110112"))

