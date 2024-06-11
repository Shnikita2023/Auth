from typing import Optional

import bcrypt
from datetime import datetime

from uuid import uuid4
from pydantic import Field as f, BaseModel

from application.domain.values.credential import Email, Password, Role, Status, FullName, Phone


class Credential(BaseModel):
    oid: str = f(default_factory=lambda: str(uuid4()))
    first_name: FullName = f(title="Имя")
    last_name: FullName = f(title="Фамилия")
    middle_name: FullName = f(title="Отчество")
    email: Email = f(title="Email")
    password: Password = f(title="Пароль")
    role: Role = f(title="Роль", default=Role.USER)
    number_phone: Phone = f(title="Номер телефона")
    time_call: str | None = f(
        title="Время звонка",
        description="Когда удобно принимать звонки",
        default=None,
        max_length=50
    )
    status: Status = f(title="Статус", default=Status.PENDING)
    created_at: datetime = f(default_factory=datetime.utcnow)

    @classmethod
    def from_json(cls, json: dict[str, str]) -> "Credential":
        return cls(
            first_name=FullName(json["first_name"]),
            last_name=FullName(json["last_name"]),
            middle_name=FullName(json["middle_name"]),
            email=Email(json["email"]),
            password=Password(json["password"] if json.get("password") else "FakePassw0rd!123"),
            number_phone=Phone(json["number_phone"]),
            time_call=json["time_call"],
            oid=json["oid"] if json.get("oid") else str(uuid4())
        )

    def to_dict(self) -> dict:
        return {
            "first_name": self.first_name.value,
            "last_name": self.last_name.value,
            "middle_name": self.middle_name.value,
            "email": self.email.value,
            "number_phone": self.number_phone.value,
            "time_call": self.time_call,
            "status": self.status.name,
            "created_at": self.created_at,
            "role": self.role.name
        }

    def encrypt_password(self, new_password: Optional[str] = None) -> None:
        salt: bytes = bcrypt.gensalt()
        if new_password:
            pwd_bytes: bytes = new_password.encode()
        else:
            pwd_bytes: bytes = self.password.value.encode()
        hashed_password: bytes = bcrypt.hashpw(pwd_bytes, salt)
        self.password = Password(hashed_password.decode())

    def is_password_valid(self, password: str) -> bool:
        return bcrypt.checkpw(password=password.encode(), hashed_password=self.password.value.encode())

    def is_status_activate(self):
        self.status = Status.ACTIVE
