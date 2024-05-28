from fastapi import Request

from application.infrastructure.brokers.producers.kafka import ProducerKafka
from application.infrastructure.db.database import async_session_maker
from application.repos.uow.unit_of_work import SqlAlchemyUnitOfWork


def get_unit_of_work() -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session_factory=async_session_maker)


def get_kafka_producer(request: Request) -> ProducerKafka:
    return request.app.state.producer_kafka
