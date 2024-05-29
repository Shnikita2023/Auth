import logging
from contextlib import asynccontextmanager
from email.message import EmailMessage
from typing import Optional

import aiosmtplib
from pydantic import EmailStr

from application.config import settings
from application.exceptions import SMTPConnectError, SMTPAuthError
from .base import EmailClient

logger = logging.getLogger(__name__)


class AIOSMTPClient(EmailClient):
    def __init__(self):
        self.smtp_hostname = settings.email.SMTP_HOST
        self.smtp_port = settings.email.SMTP_PORT
        self.smtp_user = settings.email.SMTP_USER
        self.smtp_password = settings.email.SMTP_PASSWORD
        self.client: Optional[aiosmtplib.SMTP] = None

    async def connect(self) -> aiosmtplib.SMTP:
        """Подключение к серверу SMTP"""
        try:
            self.client = aiosmtplib.SMTP(hostname=self.smtp_hostname,
                                          port=self.smtp_port,
                                          use_tls=True)
            await self.client.connect()
            logger.info("Успешное подключение к SMTP cерверу")
            await self.client.login(self.smtp_user, self.smtp_password)
            logger.info("Успешно пройдена аутентификация на SMTP сервере")
            return self.client

        except aiosmtplib.SMTPAuthenticationError:
            raise SMTPAuthError

        except (aiosmtplib.SMTPServerDisconnected, aiosmtplib.SMTPConnectError):
            raise SMTPConnectError

    async def send_notification(self, body: str, email: EmailStr, title: str):
        """Отправка сообщений"""
        try:
            message = EmailMessage()
            message["From"] = settings.email.SMTP_USER
            message["To"] = email
            message["Subject"] = title
            message.add_alternative(body, subtype='html')
            await self.client.send_message(message)

        except aiosmtplib.SMTPServerDisconnected:
            raise SMTPConnectError

    async def disconnect(self):
        """Отключение от сервера SMTP"""
        if self.client:
            self.client.close()
            logger.info("Соединение с SMTP сервером закрыто успешно")


@asynccontextmanager
async def aiosmtp_client_context(email_client: EmailClient) -> None:
    try:
        await email_client.connect()
        yield email_client
    finally:
        await email_client.disconnect()
