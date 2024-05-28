from ..client.kafka.broker import KafkaProducer
from .base import Producer


class ProducerKafka(Producer):
    def __init__(self, url: str) -> None:
        self.url = url
        self.producer = KafkaProducer()

    async def initialization(self) -> None:
        await self.producer.connect(url=self.url)

    async def delivery_message(self, message: str, topic: str) -> None:
        await self.producer.delivery_message(message=message, topic=topic)

    async def finalization(self) -> None:
        await self.producer.disconnect()
