async def test_initialization(producer_kafka):
    await producer_kafka.initialization()
    producer_kafka.producer.connect.assert_awaited_once()


async def test_delivery_message(producer_kafka):
    await producer_kafka.delivery_message(message="test message", topic="test_topic")
    producer_kafka.producer.delivery_message.assert_awaited_once_with(message="test message", topic="test_topic")


async def test_finalization(producer_kafka):
    await producer_kafka.finalization()
    producer_kafka.producer.disconnect.assert_awaited_once()
