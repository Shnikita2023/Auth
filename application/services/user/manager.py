from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from application.services.user.creator import user_creator
from application.services.user.validation import check_existing_credential
from application.web.views.user.schemas import CredentialInput, CredentialOutput


class UserManager:
    """
    Пользовательский менеджер для работы с пользователем
    """

    @staticmethod
    async def create(
            user_schema: CredentialInput,
            session: AsyncSession,
            background_tasks: BackgroundTasks) -> CredentialOutput:
        await check_existing_credential(session=session, email=user_schema.email)
        return await user_creator.create_credential(user_schema, session, background_tasks)


user_manager = UserManager()
