import bcrypt
import pytest

from application.domain.entities.credential import (
    Credential, FullName, Email,
    Password, Phone, Role, Status
)


class TestCredential:
    password = "Qwertq!2"
    new_password = "NewValidPassw0rd!"
    json_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "middle_name": "Middle",
        "email": "alice@example.com",
        "password": password,
        "number_phone": "89031110112",
        "time_call": "12:00-14:00",
    }
    credential_data = {"first_name": FullName("Alice"),
                       "last_name": FullName("Smith"),
                       "middle_name": FullName("Middle"),
                       "email": Email("alice@example.com"),
                       "number_phone": Phone("89031110112"),
                       "password": Password(password)}

    def test_new_credential_has_unique_oid(self):
        credential_one = Credential(**self.credential_data)
        credential_two = Credential(**self.credential_data)
        assert credential_one.oid != credential_two.oid

    def test_password_encryption(self):
        credential = Credential(**self.credential_data)
        credential.encrypt_password()
        assert credential.password != self.password

    def test_password_validation(self):
        hashed_password: bytes = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt())
        self.credential_data["password"] = Password(hashed_password.decode())
        credential = Credential(**self.credential_data)
        assert credential.is_password_valid(self.password) is True

    def test_is_password_valid_after_password_change(self):
        credential = Credential(**self.credential_data)
        credential.encrypt_password(self.new_password)
        assert credential.is_password_valid(self.new_password)
        assert not credential.is_password_valid(self.password)

    def test_default_values(self):
        credential = Credential(**self.credential_data)
        assert credential.role == Role.USER
        assert credential.status == Status.PENDING
        assert credential.time_call is None

    def test_is_status_activate(self):
        credential = Credential(**self.credential_data)
        assert credential.status == Status.PENDING
        credential.is_status_activate()
        assert credential.status == Status.ACTIVE

    def test_email_validation(self):
        with pytest.raises(ValueError):
            invalid_data = self.credential_data.copy()
            invalid_data["email"] = Email("invalidemail")
            Credential(**invalid_data)

    def test_phone_validation(self):
        with pytest.raises(ValueError):
            invalid_data = self.credential_data.copy()
            invalid_data["number_phone"] = Phone("12345")
            Credential(**invalid_data)

    def test_from_json(self):
        credential = Credential.from_json(self.json_data)
        assert credential.first_name.value == "Alice"
        assert credential.last_name.value == "Smith"
        assert credential.middle_name.value == "Middle"
        assert credential.email.value == "alice@example.com"
        assert credential.number_phone.value == "89031110112"
        assert credential.time_call == "12:00-14:00"

    def test_to_dict(self):
        credential = Credential(**self.credential_data)
        credential.middle_name = FullName("Middle")
        credential.time_call = "12:00-14:00"
        credential.status = Status.PENDING
        credential.role = Role.USER
        credential_dict = credential.to_dict()
        assert credential_dict["first_name"] == "Alice"
        assert credential_dict["last_name"] == "Smith"
        assert credential_dict["middle_name"] == "Middle"
        assert credential_dict["email"] == "alice@example.com"
        assert credential_dict["status"] == "PENDING"
        assert credential_dict["role"] == "USER"
        assert credential_dict["time_call"] == "12:00-14:00"
