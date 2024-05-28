from typing import AsyncGenerator, Any

import redis.asyncio as redis
from fastapi import Request
from redis.asyncio.client import Redis

from application.infrastructure.brokers.producers.kafka import ProducerKafka
from ..db.database import async_session_maker, pool_redis
from application.repos.uow.unit_of_work import SqlAlchemyUnitOfWork


def get_unit_of_work() -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session_factory=async_session_maker)


def get_kafka_producer(request: Request) -> ProducerKafka:
    return request.app.state.producer_kafka


async def get_async_redis_client() -> AsyncGenerator[Redis, Any]:
    async with redis.Redis(connection_pool=pool_redis) as redis_client:
        yield redis_client
