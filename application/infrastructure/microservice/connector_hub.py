import json

from application.infrastructure.http_client.aiohttp_client import AIOHTTPClient
from application.infrastructure.http_client.http_client_interface import HTTPClientInterface


class UserRequest:
    def __init__(self, client: HTTPClientInterface):
        self.client = client

    async def send_user_registration_data(self, url: str, data: json):
        await self.client.post(url, data)


def get_user_request():
    http_client = AIOHTTPClient()
    return UserRequest(http_client)
