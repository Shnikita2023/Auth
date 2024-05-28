import logging
from typing import Optional, Any

from fastapi import Form

from application.domain.entities.credential import Credential as DomainCredential
from application.exceptions import UserNotFoundError, UserAlreadyExistsError, InvalidUserDataError
from application.infrastructure.dependencies.dependence import get_unit_of_work
from application.repos.uow.unit_of_work import AbstractUnitOfWork

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

    async def create_user(self, user: DomainCredential) -> DomainCredential:
        params_search = {"email": user.email.value, "number_phone": user.number_phone.value}
        async with self.uow:
            existing_user = await self._check_existing_user(params_search)
            if existing_user:
                raise UserAlreadyExistsError

            user.encrypt_password()
            await self.uow.credential.add(user)
            await self.uow.commit()
            logger.info(f"Пользователь с id {user.oid} успешно создан. Status: 201")
        return user

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

    # @staticmethod
    # def check_role(role: tuple = ("USER",)) -> None:
    #     user_current = get_payload_current_user()
    #     if user_current.get("role") not in role:
    #         raise AccessDeniedError


def get_credential_service() -> CredentialService:
    return CredentialService()

