from sqlalchemy.ext.asyncio import AsyncSession

from application.domain.entities.credential import Credential as DomainCredential
from application.exceptions import UserAlreadyExistsError
from application.repos.credential import credential_db


async def check_existing_credential(session: AsyncSession, email: str) -> None:
    params_search = {"email": email}
    existing_credential: DomainCredential | None = await credential_db.get_user_by_param(session, params_search)
    if existing_credential is not None:
        raise UserAlreadyExistsError
