import logging
from typing import Any, Callable, Coroutine, Optional

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.errors import KafkaError

from app.exceptions.exception_handler import CustomKafkaError

logger = logging.getLogger(__name__)


class KafkaProducer:

    def __init__(self, topic: str) -> None:
        self.topic = topic
        self.producer: Optional[AIOKafkaProducer] = None

    async def connect(self, url: str) -> AIOKafkaProducer:
        self.producer = AIOKafkaProducer(bootstrap_servers=url)
        await self.producer.start()
        logger.info("Успешное подключение к Kafka(producers) ")
        return self.producer

    async def disconnect(self) -> None:
        if self.producer:
            await self.producer.stop()
            logger.info("Соединение с Kafka(producers) закрыто успешно")

    async def delivery_message(self, message: str) -> None:
        try:
            if self.producer:
                await self.producer.send_and_wait(topic=self.topic, value=message.encode("utf-8"))
                logger.info(msg=f"JSON message sent to kafka: {message}")

        except KafkaError as exc:
            raise CustomKafkaError(msg_exc="ошибка подключение к брокеру Kafka", status_code=500, exception=exc)


class KafkaConsumer:

    def __init__(self, group_id: str, topics: str) -> None:
        self.consumer: Optional[AIOKafkaConsumer] = None
        self.group_id = group_id
        self.topics = topics

    async def connect(self, url: str) -> AIOKafkaConsumer:
        self.consumer = AIOKafkaConsumer(self.topics, bootstrap_servers=url, group_id=self.group_id)
        await self.consumer.start()
        logger.info("Успешное подключение к Kafka(consumers)")
        return self.consumer

    async def disconnect(self) -> None:
        if self.consumer:
            await self.consumer.stop()
            logger.info("Соединение с Kafka(consumers) закрыто успешно")

    async def get_message(self, handling_message: Callable[..., Coroutine[Any, Any, None]]) -> None:

        try:
            if self.consumer:
                async for message in self.consumer:
                    await handling_message(message)

        except KafkaError as exc:
            raise CustomKafkaError(msg_exc="ошибка подключение к брокеру Kafka", status_code=500, exception=exc)
