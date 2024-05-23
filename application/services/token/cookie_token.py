import json
from datetime import datetime, timedelta

from fastapi import Response, Cookie

from application.config import settings
from application.exceptions import InvalidTokenError

COOKIE_SESSION_TIME = settings.session_cookie.COOKIE_SESSION_TIME
COOKIE_SESSION_KEY = settings.session_cookie.COOKIE_SESSION_KEY


async def create_cookie_for_tokens(response: Response,
                                   access_token: str,
                                   refresh_token: str) -> None:
    expires = datetime.utcnow() + timedelta(minutes=COOKIE_SESSION_TIME)
    expires_cookie = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
    tokens = {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
    json_data_token: str = json.dumps(tokens)
    response.set_cookie(COOKIE_SESSION_KEY,
                        json_data_token,
                        expires=expires_cookie,
                        httponly=True)


async def get_tokens_from_cookie(cookie_tokens: str = Cookie(alias=COOKIE_SESSION_KEY, default=None)) -> tuple:
    if not cookie_tokens:
        raise InvalidTokenError

    return parsing_cookie_tokens(cookie_tokens)


def parsing_cookie_tokens(cookie_tokens: str) -> tuple:
    tokens_dict = json.loads(cookie_tokens)
    return tokens_dict["access_token"], tokens_dict["refresh_token"]

# async def get_tokens_from_cookie(request: Request) -> tuple[str, str]:
#     tokens: str | None = request.cookies.get(COOKIE_SESSION_KEY)
#     try:
#         if not tokens:
#             raise InvalidTokenError
#
#         tokens_data = json.loads(tokens)
#         access_token: str = tokens_data.get("access_token")
#         refresh_token: str = tokens_data.get("refresh_token")
#         if not access_token or not refresh_token:
#             raise ValueError("No access or refresh token found")
#
#         return access_token, refresh_token
#
#     except (json.JSONDecodeError, ValueError):
#         raise InvalidTokenError
