import logging
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from application.config import settings
from application.exceptions import ApplicationException
from application.infrastructure.brokers.producers.kafka import ProducerKafka
from application.logging_config import init_logger
from application.web.views import router as router_v1

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_logger(pathname="app", filename="app.log")
    app.state.producer_kafka = ProducerKafka(url=settings.kafka.KAFKA_HOST)
    await app.state.producer_kafka.initialization()
    yield
    await app.state.producer_kafka.finalization()


main_app = FastAPI(version="1.1.1",
                   title="Auth",
                   docs_url="/api/docs",
                   debug=True,
                   lifespan=lifespan
                   )


@main_app.exception_handler(ApplicationException)
async def application_exception_handler(exc: ApplicationException):
    logger.error(msg=f"Error: {exc.message} :: Status: {exc.status_code}", exc_info=exc)
    return JSONResponse(status_code=exc.status_code, content={"status": "error",
                                                              "data": f"{datetime.now()}",
                                                              "detail": exc.message})


main_app.include_router(router_v1, prefix="/api/v1")

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)
