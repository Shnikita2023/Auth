from sqlalchemy.ext.asyncio import AsyncSession

from application.domain.entities.credential import Credential as DomainCredential
from application.domain.values.credential import Phone, Password, Email, FullName
from application.repos.credential import SQLAlchemyCredentialRepository


async def test_add_credential(credential: DomainCredential,
                              async_session: AsyncSession,
                              repo: SQLAlchemyCredentialRepository):
    added_credential = await repo.add(credential)
    await async_session.commit()
    assert added_credential.oid == credential.oid


async def test_get_credential(credential: DomainCredential,
                              async_session: AsyncSession,
                              repo: SQLAlchemyCredentialRepository):
    await repo.add(credential)
    await async_session.commit()
    fetched_credential = await repo.get(credo_oid="4aca4d42-d7cf-44dc-9081-4de782d465ff")
    assert fetched_credential is not None
    assert fetched_credential.oid == credential.oid


async def test_get_one_by_any_params(credential: DomainCredential,
                                     async_session: AsyncSession,
                                     repo: SQLAlchemyCredentialRepository):
    await repo.add(credential)
    await async_session.commit()
    params = {"email": "alice@example.com"}
    fetched_credential = await repo.get_one_by_any_params(params)
    assert fetched_credential is not None
    assert fetched_credential.email == credential.email


async def test_get_one_by_all_params(credential: DomainCredential,
                                     async_session: AsyncSession,
                                     repo: SQLAlchemyCredentialRepository):
    await repo.add(credential)
    await async_session.commit()
    params = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com"
    }
    fetched_credential = await repo.get_one_by_all_params(params)
    assert fetched_credential is not None
    assert fetched_credential.email == credential.email


async def test_update_credential(credential: DomainCredential,
                                 async_session: AsyncSession,
                                 repo: SQLAlchemyCredentialRepository):
    await repo.add(credential)
    await async_session.commit()
    updated_credential = DomainCredential(
        oid="4aca4d42-d7cf-44dc-9081-4de782d465ff",
        first_name=FullName("Jane"),
        last_name=FullName("Smith"),
        middle_name=FullName("Middle"),
        email=Email("jane.doe@example.com"),
        password=Password("Password!123"),
        time_call="in 8h",
        number_phone=Phone("89031110112"))

    await repo.update(updated_credential)
    fetched_credential = await repo.get("4aca4d42-d7cf-44dc-9081-4de782d465ff")
    assert fetched_credential is not None
    assert fetched_credential.first_name.value == "Jane"
    assert fetched_credential.email.value == "jane.doe@example.com"
