import json
import logging
from typing import Optional

import aiohttp

from .http_client_interface import HTTPClientInterface

logger = logging.getLogger(__name__)


class AIOHTTPClient(HTTPClientInterface):
    HEADERS = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    async def get(self, url: str) -> Optional[str]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status != 200:
                        raise aiohttp.ClientError(f"Ошибка при получении данных: Status {response.status}")

                    html: Optional[str] = await response.text()

            return html

        except TimeoutError as ex:
            logger.critical(msg=f"Превышена время ожидание: {ex}")

        except ConnectionError as ex:
            logger.critical(msg=f"Что-то пошло не так, попробуйте позже: {ex}")

    async def post(self, url: str, data: json) -> Optional[str]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=data, headers=self.HEADERS, timeout=5) as response:
                    if response.status != 201:
                        raise aiohttp.ClientError(f"Ошибка при получении данных: Status {response.status}")

                    html: Optional[str] = await response.text()

            return html

        except TimeoutError as ex:
            logger.critical(msg=f"Превышена время ожидание: {ex}")

        except ConnectionError as ex:
            logger.critical(msg=f"Что-то пошло не так, попробуйте позже: {ex}")
