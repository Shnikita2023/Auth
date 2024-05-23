from abc import abstractmethod, ABC
from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Response, Depends

from application.config import settings
from application.exceptions import InvalidTokenError
from application.services.token.cookie_token import get_tokens_from_cookie, create_cookie_for_tokens
from application.web.views.user.schemas import CredentialInput


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

        if len(payload) > 1:
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
            decoded: dict = jwt.decode(jwt=token, key=cls.PUBLIC_KEY, algorithms=[cls.ALGORITHM])

        except jwt.ExpiredSignatureError:
            decoded: dict = jwt.decode(jwt=token,
                                       key=cls.PUBLIC_KEY,
                                       algorithms=[cls.ALGORITHM],
                                       options={"verify_exp": False})
        return decoded


class TokenWork:
    """
    Класс для работы с токенами пользователей
    """

    def __init__(self, token_service: TokenAbstractService):
        self.token_service = token_service

    def create_tokens(self, user: CredentialInput) -> tuple:
        access_jwt_payload = {
            "sub": user.oid,
            "first_name": user.first_name,
            "email": user.email,
            "role": user.role
        }
        refresh_jwt_payload = {"sub": user.oid}
        access_token = self.token_service.encode_token(payload=access_jwt_payload)
        refresh_token = self.token_service.encode_token(payload=refresh_jwt_payload)
        return access_token, refresh_token

    def create_new_access_token(self, access_token_payload: dict) -> str:
        new_access_token: str = self.token_service.encode_token(payload=access_token_payload)
        return new_access_token

    def check_expires_tokens(self,
                             access_token_payload: dict,
                             refresh_token_payload: dict) -> str | None:
        expire_access_token = datetime.fromtimestamp(access_token_payload["exp"])
        expire_refresh_token = datetime.fromtimestamp(refresh_token_payload["exp"])
        if expire_access_token <= datetime.now() and expire_refresh_token <= datetime.now():
            raise InvalidTokenError

        if expire_access_token <= datetime.now():
            return self.create_new_access_token(access_token_payload)

        return None

    async def check_active_tokens(self, response: Response, access_token: str, refresh_token: str) -> bool:
        try:
            access_token_payload: dict = self.token_service.decode_token(token=access_token)
            refresh_token_payload: dict = self.token_service.decode_token(token=refresh_token)
            new_token: str | None = self.check_expires_tokens(access_token_payload, refresh_token_payload)

            if new_token:
                await create_cookie_for_tokens(response, new_token, refresh_token)

            return True

        except jwt.InvalidTokenError:
            raise InvalidTokenError


token_jwt_service = TokenJWTService()
token_work = TokenWork(token_jwt_service)
