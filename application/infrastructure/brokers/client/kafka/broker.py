import logging
from typing import Optional

import aiokafka

from application.exceptions import KafkaError

logger = logging.getLogger(__name__)


class KafkaProducer:

    def __init__(self) -> None:
        self.producer: Optional[aiokafka.AIOKafkaProducer] = None

    async def connect(self, url: str) -> aiokafka.AIOKafkaProducer:
        self.producer = aiokafka.AIOKafkaProducer(bootstrap_servers=url)
        await self.producer.start()
        logger.info("Успешное подключение к Kafka(producers) ")
        return self.producer

    async def disconnect(self) -> None:
        if self.producer:
            await self.producer.stop()
            logger.info("Соединение с Kafka(producers) закрыто успешно")

    async def delivery_message(self, message: str, topic: str) -> None:
        try:
            if self.producer:
                await self.producer.send_and_wait(topic=topic, value=message.encode("utf-8"))
                logger.info(msg=f"JSON message sent to kafka: {message}")

        except aiokafka.errors.KafkaError:
            raise KafkaError

