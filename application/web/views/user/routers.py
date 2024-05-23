from typing import Annotated
from fastapi import APIRouter, Depends, BackgroundTasks, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from application.config import settings
from application.infrastructure.dependencies import get_async_session
from application.infrastructure.microservice.connector_hub import UserRequest, get_user_request
from application.services.token.cookie_token import create_cookie_for_tokens, get_tokens_from_cookie
from application.services.token.schemas import TokenInfo
from application.services.token.token_jwt import token_work
from application.services.user.auth import AuthUser
from application.services.user.manager import user_manager
from application.web.views.user.schemas import CredentialOutput, CredentialInput

router = APIRouter(prefix="/user",
                   tags=["Auth"])


@router.post(path="/sign-up",
             summary="Регистрация пользователя",
             status_code=status.HTTP_201_CREATED,
             response_model=CredentialOutput)
async def register_user(user_schema: CredentialInput,
                        background_tasks: BackgroundTasks,
                        session: Annotated[AsyncSession, Depends(get_async_session)],
                        request: Annotated[UserRequest, Depends(get_user_request)]) -> CredentialOutput:
    user = await user_manager.create(user_schema=user_schema, session=session, background_tasks=background_tasks)
    await request.send_user_registration_data(url=settings.endpoint.ENDPOINT_SIGN_UP,
                                              data=user_schema.model_dump_json())
    return user


@router.post(path="/login",
             response_model=TokenInfo,
             summary="Аутентификация пользователя",
             status_code=status.HTTP_200_OK)
async def login_user(response: Response,
                     user: Annotated[CredentialOutput, Depends(AuthUser.validate_auth_user)]) -> TokenInfo:
    access_token, refresh_token = token_work.create_tokens(user=user)
    await create_cookie_for_tokens(response, access_token, refresh_token)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.get(path="/verify-tokens",
            summary="Проверка подлинности токенов",
            status_code=status.HTTP_200_OK)
async def verify_tokens(response: Response,
                        tokens: Annotated[tuple, Depends(get_tokens_from_cookie)]) -> bool:
    return await token_work.check_active_tokens(response, *tokens)


# @router.get(path="/logout", summary="Выход пользователя")
# async def logout_user(response: Response,
#                       current_user: dict = Depends(cookie_helper.get_cookie_tokens)) -> dict[str, str]:
#     response.delete_cookie(cookie_helper.COOKIE_SESSION_KEY)
#     return {"message": "logout successful"}
#

# @router.get(path="/me", summary="Получение данных о пользователе")
# async def auth_user_check_self_info(response: Response,
#                                     user: dict = Depends(AuthUser.get_current_auth_user)) -> dict:
#     return {
#         "id": user["sub"],
#         "username": user["username"],
#         "email": user["email"]
#     }


# @router.post(path="/forgot_password", summary="Восстановление пароля пользователя")
# async def forgot_password(forgot_data: ForgotUser,
#                           session: AsyncSession = Depends(get_async_session),
#                           redis_client: Redis = Depends(get_async_redis_client)) -> dict:
#     return await PasswordForgot(user_email=forgot_data.email,
#                                 session=session,
#                                 redis_client=redis_client).forgot_password_user()
#
#
# @router.post(path="/reset_password", summary="Сброс пароля пользователя")
# async def reset_password(reset_data: ResetUser,
#                          session: AsyncSession = Depends(get_async_session),
#                          redis_client: Redis = Depends(get_async_redis_client)):
#     return await PasswordReset(token=reset_data.token,
#                                password=reset_data.password,
#                                user_email=reset_data.email,
#                                session=session,
#                                redis_client=redis_client).reset_password_user()
