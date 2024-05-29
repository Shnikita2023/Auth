import logging

from pydantic import EmailStr

from application.infrastructure.email_service.client.aiosmtp_client import AIOSMTPClient, aiosmtp_client_context

logger = logging.getLogger(__name__)
URL: str = "http://127.0.0.1:8002/api/v1/auth/"


async def send_password_reset_email(email: EmailStr, token: str) -> None:
    """Отправка сообщение о сбросе пароля"""
    body = f"Для сброса пароля перейдите по ссылке: {URL}reset-password?token={token}"
    title = "Сброс пароля"

    async with aiosmtp_client_context(AIOSMTPClient()) as client:
        await client.send_notification(body=body, email=email, title=title)
        logger.info(f"Успешная отправка письма о сбросе пароля на {email}")


async def send_letter_on_activate_account(email: EmailStr, activation_code: str) -> None:
    """Отправка сообщение об успешной регистрации"""
    body = f"Привет, перейдите по ссылке для активации аккаунта:: {URL}activate?code={activation_code}"
    title = "Активация аккаунта"

    async with aiosmtp_client_context(AIOSMTPClient()) as client:
        await client.send_notification(body=body, email=email, title=title)
        logger.info(f"Успешная отправка письма о регистрации на {email}")
