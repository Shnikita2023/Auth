from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Request, Depends

from application.config import settings
from application.exceptions.domain import InvalidTokenError
from application.services.user import UserService
from application.web.views.user.schemas import UserOutput

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


class TokenAbstractService(ABC):
    @abstractmethod
    def encode_token(self, payload: dict) -> str:
        raise NotImplemented

    @abstractmethod
    def decode_token(self, token: bytes | str) -> dict:
        raise NotImplemented


class TokenJWTService(TokenAbstractService):
    """
    Класс для кодирования/декодирование jwt токена
    """

    ACCESS_TOKEN_EXPIRE_MINUTE: int = settings.auth_jwt.ACCESS_TOKEN_EXPIRE_MINUTE
    REFRESH_TOKEN_EXPIRE_MINUTE: int = settings.auth_jwt.REFRESH_TOKEN_EXPIRE_MINUTE
    PRIVATE_KEY: str = settings.auth_jwt.PRIVATE_KEY.read_text()
    PUBLIC_KEY: str = settings.auth_jwt.PUBLIC_KEY.read_text()
    ALGORITHM: str = settings.auth_jwt.ALGORITHM

    @classmethod
    def encode_token(cls, payload: dict) -> str:

        if payload["type"] == ACCESS_TOKEN_TYPE:
            expire_minutes = cls.ACCESS_TOKEN_EXPIRE_MINUTE
        else:
            expire_minutes = cls.REFRESH_TOKEN_EXPIRE_MINUTE

        to_encode: dict = payload.copy()
        now_time: datetime = datetime.utcnow()
        expire_token: datetime = now_time + timedelta(minutes=expire_minutes)
        to_encode.update(exp=expire_token, iat=now_time)
        encoded: str = jwt.encode(payload=to_encode, key=cls.PRIVATE_KEY, algorithm=cls.ALGORITHM)
        return encoded

    @classmethod
    def decode_token(cls, token: bytes | str) -> dict:
        try:
            return jwt.decode(jwt=token, key=cls.PUBLIC_KEY, algorithms=[cls.ALGORITHM])

        except jwt.ExpiredSignatureError:
            raise InvalidTokenError


class TokenManager:
    """
    Класс для работы с токенами пользователей
    """

    def __init__(self, token_service: TokenAbstractService):
        self.token_service = token_service

    def create_token(self, user_schema: UserOutput, type_token: str) -> str:
        if type_token == ACCESS_TOKEN_TYPE:
            jwt_payload: dict = {"sub": user_schema.oid,
                                 "first_name": user_schema.first_name,
                                 "email": user_schema.email,
                                 "role": user_schema.role,
                                 "type": ACCESS_TOKEN_TYPE}
        else:
            jwt_payload: dict = {"sub": user_schema.oid, "type": REFRESH_TOKEN_TYPE}

        return self.token_service.encode_token(payload=jwt_payload)

    async def get_current_token_payload(self, request: Request) -> dict:
        try:
            payload: str | None = request.headers.get('Authorization')
            if not payload:
                raise InvalidTokenError

            token: str = payload.split()[1]
            return self.token_service.decode_token(token=token)

        except jwt.InvalidTokenError:
            raise InvalidTokenError

    async def get_auth_user_from_token_of_type(self,
                                               payload: dict,
                                               token_type: str) -> UserOutput:
        self.validate_token_type(payload, token_type)
        return await self.get_user_by_token_sub(payload)

    @staticmethod
    async def get_user_by_token_sub(payload: dict) -> UserOutput:
        user_oid: str | None = payload.get("sub")
        user = await UserService().get_user_by_id(user_oid)
        return UserOutput.to_schema(user)

    @staticmethod
    def validate_token_type(payload: dict, token_type: str) -> bool:
        current_token_type = payload.get("type")
        if current_token_type == token_type:
            return True

        raise InvalidTokenError


token_jwt_service = TokenJWTService()
token_manager = TokenManager(token_jwt_service)
