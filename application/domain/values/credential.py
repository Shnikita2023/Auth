import re
from dataclasses import dataclass
from enum import Enum

from application.constants import (
    EMAIL_ERROR, PASSWORD_LENGTH_ERROR,
    PASSWORD_UPPERCASE_ERROR, PASSWORD_SPECIAL_CHAR_ERROR,
    PASSWORD_DIGIT_ERROR, PASSWORD_LOWERCASE_ERROR, PHONE_ERROR, FULLNAME_ERROR
)
from application.domain.values.base import BaseValueObjects


@dataclass(frozen=True, slots=True)
class Email(BaseValueObjects):
    value: str

    def validate(self) -> None:
        EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        # Проверка формата email
        if not re.match(EMAIL_REGEX, self.value):
            raise ValueError(EMAIL_ERROR)


@dataclass(frozen=True, slots=True)
class Password(BaseValueObjects):
    value: str

    def validate(self) -> None:
        PASSWORD_REGEX = r"[!@#$%^&*()\-_=+{};:,<.>|\[\]\\/?]"

        # Проверка на длину пароля
        if len(self.value) < 8 or len(self.value) > 100:
            raise ValueError(PASSWORD_LENGTH_ERROR)

        # Проверка на наличие хотя бы одной заглавной буквы
        if not any(c.isupper() for c in self.value):
            raise ValueError(PASSWORD_UPPERCASE_ERROR)

        # Проверка на наличие хотя бы одной строчной буквы
        if not any(c.islower() for c in self.value):
            raise ValueError(PASSWORD_LOWERCASE_ERROR)

        # Проверка на наличие хотя бы одной цифры
        if not any(c.isdigit() for c in self.value):
            raise ValueError(PASSWORD_DIGIT_ERROR)

        # Проверка на наличие хотя бы одного специального символа
        if not re.search(PASSWORD_REGEX, self.value):
            raise ValueError(PASSWORD_SPECIAL_CHAR_ERROR)


@dataclass(frozen=True, slots=True)
class Phone(BaseValueObjects):
    value: str

    def validate(self) -> None:
        if not self.value.startswith(("7", "8")) or not self.value.isdigit() or len(self.value) != 11:
            raise ValueError(PHONE_ERROR)


@dataclass(frozen=True, slots=True)
class FullName(BaseValueObjects):
    value: str

    def validate(self) -> None:
        username_regex = r"^[А-ЯЁ][а-яё]+$|^[A-Z][a-z]+$"
        if not re.match(username_regex, self.value) or len(self.value) > 50:
            raise ValueError(FULLNAME_ERROR)


class Role(str, Enum):
    ADMIN = "Администратор"
    GUEST = "Гость"
    USER = "Пользователь"
    MODERATOR = "Модератор"


class Status(str, Enum):
    ACTIVE = "Активный"
    BLOCKED = "Заблокирован"
    PENDING = "Ожидает подтверждение email"
