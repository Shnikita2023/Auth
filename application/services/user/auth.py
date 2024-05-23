import logging
from typing import Annotated

from fastapi import Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from application.domain.entities.credential import Credential as DomainCredential
from application.exceptions import InvalidUserDataError
from application.infrastructure.dependencies import get_async_session
from application.repos.credential import credential_db
from application.web.views.user.schemas import CredentialOutput

logger = logging.getLogger(__name__)


class AuthUser:
    """
    Класс для валидация пользователя
    """
    @staticmethod
    async def validate_auth_user(session: Annotated[AsyncSession, Depends(get_async_session)],
                                 email: str = Form(),
                                 password: str = Form()) -> CredentialOutput:
        params_search = {"email": email, "status": "ACTIVE"}
        user: DomainCredential | None = await credential_db.get_user_by_param(session, params_search)
        if not user or email != user.email.value or not user.is_password_valid(password):
            raise InvalidUserDataError

        logger.info(f"Успешно пройдена валидация пользователя '{user.first_name}'. Status: 200")
        return CredentialOutput.to_schema(user)

    #
    # @staticmethod
    # async def get_current_auth_user(response: Response,
    #                                 payload: dict = Depends(TokenWork.check_active_token),
    #                                 session: AsyncSession = Depends(get_async_session)) -> dict:
    #     user_id: int = payload.get("sub")
    #     user: User | None = await UserValidator.validate_user_data_by_field(session=session,
    #                                                                         value=user_id)
    #     if user_id == user.id:
    #         logger.info(f"Получение данных о пользователе '{user.username}'. Status: 200")
    #         return payload
    #
    #     raise HttpAPIException(exception="user not found").http_error_401
