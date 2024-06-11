from typing import Final
from unittest.mock import AsyncMock, patch

from application.infrastructure.brokers.client.kafka.broker import KafkaProducer

URL: Final[str] = "test_url"


async def test_connect_successful(broker_kafka: KafkaProducer) -> None:
    with patch("aiokafka.AIOKafkaProducer.start") as kafka_connect_mock:
        connection_mock = AsyncMock()
        kafka_connect_mock.return_value = connection_mock
        await broker_kafka.connect(URL)

    kafka_connect_mock.assert_called_once()
    assert kafka_connect_mock.await_count == 1


async def test_disconnect(broker_kafka):
    broker_kafka.producer = AsyncMock()
    await broker_kafka.disconnect()
    broker_kafka.producer.stop.assert_awaited_once()


async def test_delivery_message(broker_kafka):
    broker_kafka.producer = AsyncMock()
    message = "test message"
    topic = "test_topic"
    await broker_kafka.delivery_message(message, topic)
    broker_kafka.producer.send_and_wait.assert_awaited_once_with(topic=topic, value=message.encode("utf-8"))
