from unittest.mock import AsyncMock

import pytest

from application.infrastructure.email_service.client.aiosmtp_client import AIOSMTPClient


@pytest.fixture
def smtp_client() -> AIOSMTPClient:
    return AIOSMTPClient()

