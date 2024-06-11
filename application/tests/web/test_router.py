from fastapi import status, Response
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch

from application.domain.entities.credential import Credential as DomainCredential
from application.web.app import main_app

user_data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "Padhb675@",
    "number_phone": "79991114442",
    "middle_name": "Middle",
    "time_call": "in 8h"
}

expected_response = {
    "oid": "e854de2d-e873-48e4-8459-5dc4f7fdc5c5",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "number_phone": "79991114442",
    "middle_name": "Middle",
    "time_call": "in 8h",
    "role": "USER",
    "status": "Ожидает подтверждение email"
}


async def test_add_user(async_client: AsyncClient) -> None:
    mock_credential_service = AsyncMock()
    mock_kafka_producer = AsyncMock()
    mock_redis_client = AsyncMock()
    main_app.state.producer_kafka = mock_kafka_producer

    with (
        patch("application.services.user.user.CredentialService",
              return_value=mock_credential_service),
        patch("application.infrastructure.dependencies.dependence.get_async_redis_client",
              return_value=mock_redis_client)
    ):
        mock_credential_service.create_user.return_value = DomainCredential.from_json(expected_response)

        response: Response = await async_client.post(url="/api/v1/auth/sign-up", json=user_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == expected_response

        mock_credential_service.create_user.assert_awaited_once()
        assert mock_credential_service.create_user.call_args[1]["user"].email.value == user_data["email"]
        assert mock_credential_service.create_user.call_args[1]["user"].first_name.value == user_data["first_name"]

        mock_kafka_producer.delivery_message.assert_not_called()
        mock_redis_client.set.assert_not_called()

        assert response.headers["Content-Type"] == "application/json"
