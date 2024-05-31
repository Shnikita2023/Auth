import asyncio
import logging
import secrets
from typing import Optional, Any

from fastapi import Form, BackgroundTasks
from redis.asyncio import Redis

from application.config import settings
from application.domain.entities.credential import Credential as DomainCredential
from application.events import UserRegisteredEvent, UserUpdatedStatusEvent
from application.exceptions import UserNotFoundError, UserAlreadyExistsError, InvalidUserDataError, AccountActivateError
from application.infrastructure.brokers.producers.kafka import ProducerKafka
from application.infrastructure.dependencies.dependence import get_unit_of_work
from application.infrastructure.email_service.send_letter import send_letter_on_activate_account
from application.repos.uow.unit_of_work import AbstractUnitOfWork
from application.services.user.utils import (
    PasswordForgot, PasswordReset,
    save_activation_code_to_redis, check_activation_code_from_redis

)

logger = logging.getLogger(__name__)


class CredentialService:
    uow: AbstractUnitOfWork

    def __init__(self, uow=None):
        self.uow = uow if uow else get_unit_of_work()

    async def get_user_by_id(self, user_oid: str) -> DomainCredential:
        async with self.uow:
            user: Optional[DomainCredential] = await self.uow.credential.get(user_oid)
            if user:
                return user
            raise UserNotFoundError

    async def create_user(self,
                          user: DomainCredential,
                          background_tasks: BackgroundTasks,
                          redis_client: Redis,
                          kafka_producer: ProducerKafka) -> DomainCredential:
        params_search = {"email": user.email.value, "number_phone": user.number_phone.value}
        async with self.uow:
            existing_user = await self._check_existing_user(params_search)
            if existing_user:
                raise UserAlreadyExistsError

            user.encrypt_password()
            await self.uow.credential.add(user)
            await self.uow.commit()
            background_tasks.add_task(self._on_after_create_user, user, redis_client)
            broker_message = UserRegisteredEvent(message=user.to_dict())
            asyncio.create_task(kafka_producer.delivery_message(message=broker_message.to_json(),
                                                                topic=settings.kafka.USER_TOPIC))
            logger.info(f"Пользователь с id {user.oid} успешно создан. Status: 201")
        return user

    @staticmethod
    async def _on_after_create_user(user: DomainCredential, redis_client: Redis) -> None:
        activation_code: str = secrets.token_urlsafe(16)
        await asyncio.gather(
            save_activation_code_to_redis(user_oid=user.oid, redis_client=redis_client, code=activation_code),
            send_letter_on_activate_account(email=user.email.value, activation_code=activation_code)
        )

    async def _check_existing_user(self, params_search: dict[str, Any]) -> Optional[DomainCredential]:
        return await self.uow.credential.get_one_by_any_params(params_search)

    async def validate_auth_user(self,
                                 email: str = Form(),
                                 password: str = Form()) -> DomainCredential:
        params_search = {"email": email, "status": "ACTIVE"}
        async with self.uow:
            user: DomainCredential | None = await self.uow.credential.get_one_by_all_params(params_search)
            if not user or email != user.email.value or not user.is_password_valid(password):
                raise InvalidUserDataError
            logger.info(f"Успешно пройдена валидация пользователя '{user.first_name}'. Status: 200")
        return user

    async def forgot_password_user(self,
                                   email: str,
                                   redis_client: Redis) -> str:
        async with self.uow:
            params_search = {"email": email}
            credential: DomainCredential | None = await self.uow.credential.get_one_by_all_params(params_search)
            if not credential:
                raise UserNotFoundError
            return await PasswordForgot().forgot_password(redis_client=redis_client,
                                                          user_oid=credential.oid)

    async def reset_password_user(self,
                                  email: str,
                                  new_password: str,
                                  token: str,
                                  redis_client: Redis) -> None:
        async with self.uow:
            params_search = {"email": email}
            credential: DomainCredential | None = await self.uow.credential.get_one_by_all_params(params_search)
            if not credential:
                raise UserNotFoundError
            await PasswordReset().reset_password(redis_client=redis_client,
                                                 user_oid=credential.oid,
                                                 token=token)
            credential.encrypt_password(new_password)
            await self.uow.credential.update(credo=credential)
            await self.uow.commit()

    async def validate_activation_code(self, code: str, redis_client: Redis, kafka_producer: ProducerKafka):
        user_oid: str = await check_activation_code_from_redis(redis_client, code)
        user: DomainCredential = await self.get_user_by_id(user_oid)
        if user.status.name == "ACTIVE":
            raise AccountActivateError

        user.encrypt_password()
        user.is_status_activate()
        async with self.uow:
            await self.uow.credential.update(credo=user)
            await self.uow.commit()
        broker_message = UserUpdatedStatusEvent(message=user.to_dict())
        asyncio.create_task(kafka_producer.delivery_message(message=broker_message.to_json(),
                                                            topic=settings.kafka.USER_TOPIC))


def get_credential_service() -> CredentialService:
    return CredentialService()
