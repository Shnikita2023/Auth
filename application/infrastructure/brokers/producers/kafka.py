from ..client.kafka.broker import KafkaProducer
from ..client.schemas import ConnectionParamsKafka
from .base import Producer


class ProducerKafka(Producer):
    def __init__(self, data: ConnectionParamsKafka) -> None:
        self.data = data
        self.producer = KafkaProducer(topic=data.topic)

    async def initialization(self) -> None:
        await self.producer.connect(url=self.data.url)

    async def delivery_message(self, message: str) -> None:
        await self.producer.delivery_message(message=message)

    async def finalization(self) -> None:
        await self.producer.disconnect()
