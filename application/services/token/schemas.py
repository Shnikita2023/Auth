from pydantic import BaseModel


class TokenInfo(BaseModel):
    """
    Класс для создания модели токена
    """

    refresh_token: str
    access_token: str
    token_type: str = "Bearer"
