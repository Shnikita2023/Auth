import secrets

from redis.asyncio.client import Redis
from redis import RedisError

from application.exceptions import RedisTokenError


class PasswordForgot:
    """
    Класс для восстановления пароля пользователя
    """

    async def forgot_password(self, redis_client: Redis, email: str, user_oid: str) -> dict:
        token: str = self.generate_temporary_token()
        await self.set_token_by_redis(user_id=user_oid,
                                      token=token,
                                      redis_client=redis_client)
        # TODO нужна реализовать отправку токена на емайл
        # await send_password_reset_email(email=user.email, token=token)
        return {"message": "На ваш email отправлена ссылка на сброс пароля"}

    @staticmethod
    async def set_token_by_redis(user_id: str, token: str, redis_client: Redis) -> str:
        try:
            await redis_client.setex(name=f"user_{user_id}", value=token, time=6000)
            return token

        except RedisError:
            raise RedisTokenError

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
            raise RedisTokenError
