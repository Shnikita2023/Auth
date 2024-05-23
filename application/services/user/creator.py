import logging

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from application.domain.entities.credential import Credential as DomainCredential
from application.repos.credential import credential_db
from application.web.views.user.schemas import CredentialInput, CredentialOutput

logger = logging.getLogger(__name__)


class UserCreator:
    """
    Класс для создания пользователя
    """

    async def create_credential(self,
                                user_schema: CredentialInput,
                                session: AsyncSession,
                                background_tasks: BackgroundTasks) -> CredentialOutput:
        credential: DomainCredential = user_schema.to_domain()
        credential.encrypt_password()
        created_credo: DomainCredential = await credential_db.add(session=session, credo=credential)
        background_tasks.add_task(self._on_after_register, created_credo)
        logger.info(f"Учётные данные с id {created_credo.oid} успешно создан. Status: 201")
        return CredentialOutput.to_schema(credential)

    @staticmethod
    async def _on_after_register(user_schema: CredentialInput) -> None:
        pass


user_creator = UserCreator()
