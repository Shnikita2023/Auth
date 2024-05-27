from pydantic import BaseModel, Field as f


class TokenInfo(BaseModel):
    refresh_token: str | None = f(default=None)
    access_token: str
    token_type: str = f(default="Bearer")
