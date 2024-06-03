from datetime import datetime
from uuid import UUID

from sqlalchemy import String, text, types, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from application.domain.entities.credential import Credential as DomainCredential
from application.domain.values.credential import FullName, Email, Phone, Role, Status, Password
from application.repos.models.base import Base


class Credential(Base):
    __tablename__ = "сredential"

    oid: Mapped[UUID] = mapped_column(types.Uuid,
                                      primary_key=True,
                                      server_default=text("gen_random_uuid()"))
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    middle_name: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password: Mapped[bytes] = mapped_column(LargeBinary)
    role: Mapped[str]
    number_phone: Mapped[str] = mapped_column(String(11), unique=True, index=True)
    time_call: Mapped[str] = mapped_column(String(50))
    status: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    def to_entity(self) -> DomainCredential:
        decode_password = str(self.password, "utf-8")
        return DomainCredential(
            oid=str(self.oid),
            first_name=FullName(self.first_name),
            last_name=FullName(self.last_name),
            middle_name=FullName(self.middle_name),
            email=Email(self.email),
            password=Password(decode_password),
            number_phone=Phone(self.number_phone),
            role=Role[self.role],
            time_call=self.time_call,
            status=Status[self.status],
            created_at=self.created_at
        )

    @classmethod
    def from_entity(cls, credential: DomainCredential) -> "Credential":
        return cls(
            oid=credential.oid,
            first_name=credential.first_name.value,
            last_name=credential.last_name.value,
            middle_name=credential.middle_name.value,
            email=credential.email.value,
            password=credential.password.value.encode(),
            role=credential.role.name,
            number_phone=credential.number_phone.value,
            time_call=credential.time_call,
            status=credential.status.name,
            created_at=credential.created_at
        )

    @staticmethod
    def to_dict(credential: DomainCredential) -> dict[str, str]:
        return {
            "oid": credential.oid,
            "first_name": credential.first_name.value,
            "last_name": credential.last_name.value,
            "middle_name": credential.middle_name.value,
            "password": credential.password,
            "email": credential.email.value,
            "role": credential.role.name,
            "number_phone": credential.number_phone.value,
            "time_call": credential.time_call,
            "status": credential.status.name
        }
