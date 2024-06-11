from unittest.mock import AsyncMock, patch


async def test_connect_successful(smtp_client):
    with patch('aiosmtplib.SMTP') as smtp_mock:
        smtp_instance = smtp_mock.return_value
        smtp_instance.connect = AsyncMock()
        smtp_instance.login = AsyncMock()

        await smtp_client.connect()

        smtp_mock.assert_called_once_with(hostname=smtp_client.smtp_hostname,
                                          port=smtp_client.smtp_port,
                                          use_tls=True)
        smtp_instance.connect.assert_awaited_once()
        smtp_instance.login.assert_awaited_once_with(smtp_client.smtp_user,
                                                     smtp_client.smtp_password)


async def test_send_notification(smtp_client):
    smtp_client.client = AsyncMock()
    body = "<h1>Test email</h1>"
    email = "test@example.com"
    title = "Test email"
    await smtp_client.send_notification(body, email, title)
    message = smtp_client.client.send_message.call_args[0][0]
    assert message['From'] == smtp_client.smtp_user
    assert message['To'] == email
    assert message['Subject'] == title
    html_part = next(part for part in message.walk() if part.get_content_subtype() == 'html')
    assert html_part.get_content_type() == 'text/html'
    assert html_part.get_payload().strip() == body.strip()


async def test_disconnect(smtp_client):
    smtp_client.client = AsyncMock()
    await smtp_client.disconnect()
    smtp_client.client.close.assert_called_once()
