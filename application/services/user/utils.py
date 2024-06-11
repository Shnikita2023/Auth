import secrets
from typing import Optional

from application.exceptions import RedisTokenError, RedisCodeError
from application.infrastructure.cache.redis import with_redis_store, RedisCacheStore


class PasswordForgot:
    """
    Класс для восстановления пароля пользователя
    """

    async def forgot_password(self, user_oid: str) -> str:
        token: str = self.generate_temporary_token()
        await self.set_token_by_redis(user_id=user_oid,
                                      token=token)
        return token

    @staticmethod
    @with_redis_store(prefix="user")
    async def set_token_by_redis(redis_store: RedisCacheStore, user_id: str, token: str) -> None:
        await redis_store.set(key=user_id, value=token, expire_at=6000)

    @staticmethod
    def generate_temporary_token() -> str:
        token: str = secrets.token_hex(32)
        return token


class PasswordReset:
    """
    Класс для сброса пароля пользователя
    """

    async def reset_password(self,
                             token: str,
                             user_oid: str) -> None:
        await self.verify_temporary_token(token=token,
                                          user_oid=user_oid)

    @staticmethod
    @with_redis_store(prefix="user")
    async def verify_temporary_token(redis_store: RedisCacheStore,
                                     token: str,
                                     user_oid: str) -> bool:
        token_key: str = await redis_store.get(user_oid)

        if token == token_key:
            return True

        raise RedisTokenError


@with_redis_store(prefix="code")
async def save_activation_code_to_redis(redis_store: RedisCacheStore, user_oid: str, code: str) -> None:
    data: str = f"{code} {user_oid}"
    await redis_store.set(key=code, value=data)


@with_redis_store(prefix="code")
async def check_activation_code_from_redis(redis_store: RedisCacheStore, code: str) -> str:
    data: Optional[str] = await redis_store.get(code)

    if not data:
        raise RedisCodeError

    activate_code, user_oid = data.split()
    if activate_code != code:
        raise RedisCodeError

    return user_oid
