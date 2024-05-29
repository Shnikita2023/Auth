import secrets

from redis.asyncio.client import Redis
from redis import RedisError

from application.exceptions import RedisTokenError, RedisCodeError, RedisConnectError


class PasswordForgot:
    """
    Класс для восстановления пароля пользователя
    """

    async def forgot_password(self, redis_client: Redis, user_oid: str) -> str:
        token: str = self.generate_temporary_token()
        await self.set_token_by_redis(user_id=user_oid,
                                      token=token,
                                      redis_client=redis_client)
        return token

    @staticmethod
    async def set_token_by_redis(user_id: str, token: str, redis_client: Redis) -> None:
        try:
            await redis_client.setex(name=f"user_{user_id}", value=token, time=6000)

        except RedisError:
            raise RedisConnectError

    @staticmethod
    def generate_temporary_token() -> str:
        token: str = secrets.token_hex(32)
        return token


class PasswordReset:
    """
    Класс для сброса пароля пользователя
    """

    async def reset_password(self,
                             redis_client: Redis,
                             token: str,
                             user_oid: str) -> None:
        await self.verify_temporary_token(token=token,
                                          redis_client=redis_client,
                                          user_oid=user_oid)

    @staticmethod
    async def verify_temporary_token(token: str,
                                     redis_client: Redis,
                                     user_oid: str) -> bool:
        try:
            token_key: str = await redis_client.get(f"user_{user_oid}")

            if token == token_key:
                return True

            raise RedisTokenError

        except RedisError:
            raise RedisConnectError


async def save_activation_code_to_redis(user_oid: str, redis_client: Redis, code: str) -> None:
    try:
        data: str = f"{code} {user_oid}"
        await redis_client.setex(name=f"code_{code}", value=data, time=86400)

    except RedisError:
        raise RedisConnectError


async def check_activation_code_from_redis(redis_client: Redis, code: str) -> str:
    try:
        data: str = await redis_client.get(f"code_{code}")
        if not data:
            raise RedisCodeError

        activate_code, user_oid = data.split()
        if activate_code != code:
            raise RedisCodeError

        return user_oid

    except RedisError:
        raise RedisConnectError
