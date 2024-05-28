import asyncio
from typing import Annotated
from fastapi import APIRouter, Depends, status
from redis.asyncio import Redis

from application.config import settings
from application.domain.entities.credential import Credential as DomainCredential
from application.events import UserRegisteredEvent
from application.infrastructure.brokers.producers.kafka import ProducerKafka
from application.infrastructure.dependencies.dependence import get_kafka_producer, get_async_redis_client
from application.services.user import get_credential_service, CredentialService
from application.web.services.token.schemas import TokenInfo
from application.web.services.token.token_jwt import token_manager, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from application.web.views.user.schemas import CredentialOutput, CredentialInput, ForgotUser, ResetUser

router = APIRouter(prefix="/auth",
                   tags=["Auth"])


@router.post(path="/sign-up",
             summary="Регистрация пользователя",
             response_model=CredentialOutput,
             status_code=status.HTTP_201_CREATED)
async def add_user(credo_service: Annotated[CredentialService, Depends(get_credential_service)],
                   kafka_producer: Annotated[ProducerKafka, Depends(get_kafka_producer)],
                   credo_schema: CredentialInput) -> CredentialOutput:
    user = await credo_service.create_user(user=credo_schema.to_domain())
    broker_message = UserRegisteredEvent(message=credo_schema.model_dump())
    asyncio.create_task(kafka_producer.delivery_message(message=broker_message.to_json(),
                                                        topic=settings.kafka.USER_TOPIC))
    return CredentialOutput.to_schema(user)


@router.post(path="/login",
             response_model=TokenInfo,
             summary="Аутентификация пользователя",
             status_code=status.HTTP_200_OK)
async def login_user(
        user: Annotated[DomainCredential, Depends(get_credential_service().validate_auth_user)]
) -> TokenInfo:
    credo_schema = CredentialOutput.to_schema(user)
    access_token = token_manager.create_token(credo_schema=credo_schema, type_token=ACCESS_TOKEN_TYPE)
    refresh_token = token_manager.create_token(credo_schema=credo_schema, type_token=REFRESH_TOKEN_TYPE)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post(path="/refresh",
             response_model=TokenInfo,
             response_model_exclude_none=True,
             summary="Обновление access токена",
             status_code=status.HTTP_200_OK)
async def refresh_access_token(payload: Annotated[dict, Depends(token_manager.get_current_token_payload)]) -> TokenInfo:
    credo_schema = await token_manager.get_auth_user_from_token_of_type(payload, REFRESH_TOKEN_TYPE)
    access_token = token_manager.create_token(credo_schema=credo_schema, type_token=ACCESS_TOKEN_TYPE)
    return TokenInfo(access_token=access_token)


@router.post(path="/forgot-password",
             summary="Восстановление пароля пользователя",
             status_code=status.HTTP_200_OK)
async def forgot_password(forgot_schema: ForgotUser,
                          credo_service: Annotated[CredentialService, Depends(get_credential_service)],
                          redis_client: Redis = Depends(get_async_redis_client)) -> dict:
    await credo_service.forgot_password_user(email=forgot_schema.email, redis_client=redis_client)
    return {"message": "На ваш email отправлена ссылка на сброс пароля"}


@router.patch(path="/reset_password",
              summary="Сброс пароля пользователя",
              status_code=status.HTTP_200_OK)
async def reset_password(reset_schema: ResetUser,
                         credo_service: Annotated[CredentialService, Depends(get_credential_service)],
                         redis_client: Redis = Depends(get_async_redis_client)):
    await credo_service.reset_password_user(email=reset_schema.email,
                                            new_password=reset_schema.password,
                                            token=reset_schema.token,
                                            redis_client=redis_client)
    return {"message": "Пароль успешно сброшен и установлен новый"}
