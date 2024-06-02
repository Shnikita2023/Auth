from dataclasses import dataclass


class ApplicationException(Exception):
    text: str
    status_code: int = 500

    @property
    def message(self) -> str:
        return "Что-то пошло не так, попробуйте позже"


@dataclass(eq=False)
class PasswordValidationError(ApplicationException):
    text: str
    status_code = 400

    @property
    def message(self) -> str:
        return f"Неверный формат: {self.text}"


@dataclass(eq=False)
class EmailValidationError(ApplicationException):
    text: str
    status_code = 400

    @property
    def message(self) -> str:
        return f"Неверный формат: {self.text}"


@dataclass(eq=False)
class FullNameValidationError(ApplicationException):
    text: str
    status_code = 400

    @property
    def message(self) -> str:
        return (f"Неверный формат поля: {self.text}, должно содержать от 2 до 50 символов, "
                f"только латинские буквы и начинаться с большой буквы, затем строчные")


@dataclass(eq=False)
class PhoneValidationError(ApplicationException):
    text: str
    status_code = 400

    @property
    def message(self) -> str:
        return f"Неверный формат поля phone: {self.text}, должно содержать 11 цифр и начинаться с 7 или 8"


@dataclass(eq=False)
class UserAlreadyExistsError(ApplicationException):
    status_code = 400

    @property
    def message(self) -> str:
        return "The user already exists"


@dataclass(eq=False)
class UserNotFoundError(ApplicationException):
    status_code = 400

    @property
    def message(self) -> str:
        return "The user was not found"


@dataclass(eq=False)
class InvalidUserDataError(ApplicationException):
    status_code = 400

    @property
    def message(self) -> str:
        return "Invalid username or password"


@dataclass(eq=False)
class DBError(ApplicationException):
    exception: Exception

    @property
    def message(self) -> str:
        return "Ошибка подключение к базе данных"


@dataclass(eq=False)
class InvalidTokenError(ApplicationException):
    status_code = 401

    @property
    def message(self) -> str:
        return "Invalid token"


@dataclass(eq=False)
class KafkaError(ApplicationException):
    status_code = 500

    @property
    def message(self) -> str:
        return "Ошибка подключение к брокеру Kafka"


@dataclass(eq=False)
class RedisTokenError(ApplicationException):
    status_code = 500

    @property
    def message(self) -> str:
        return "Ошибка работы с временным токеном"


@dataclass(eq=False)
class RedisCodeError(ApplicationException):
    status_code = 400

    @property
    def message(self) -> str:
        return "Неверный код активации"


@dataclass(eq=False)
class RedisConnectError(ApplicationException):
    status_code = 500

    @property
    def message(self) -> str:
        return "Ошибка работы с Redis"


@dataclass(eq=False)
class SMTPConnectError(ApplicationException):
    status_code = 500

    @property
    def message(self) -> str:
        return "Ошибка подключение к SMTP серверу"


@dataclass(eq=False)
class SMTPAuthError(ApplicationException):
    status_code = 500

    @property
    def message(self) -> str:
        return "Ошибка аутентификации с SMTP сервером"


@dataclass(eq=False)
class AccessDeniedError(ApplicationException):
    status_code = 403

    @property
    def message(self) -> str:
        return "Access denied"


@dataclass(eq=False)
class AccountActivateError(ApplicationException):
    status_code = 400

    @property
    def message(self) -> str:
        return "Аккаунт уже активирован"
