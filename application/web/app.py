import logging
from contextlib import asynccontextmanager
from datetime import datetime

import sentry_sdk
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware

from application.config import settings
from application.exceptions import ApplicationException
from application.infrastructure.brokers.producers.kafka import ProducerKafka
from application.logging_config import init_logger
from application.web.views import router as router_v1

logger = logging.getLogger(__name__)

sentry_sdk.init(
    dsn="https://6a4f782139a6155faabe13ac33067ecc@o4505980199305216.ingest.us.sentry.io/4507476922466304",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = FastAPI()


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
async def application_exception(request: Request, exc: ApplicationException) -> JSONResponse:
    logger.error(msg=f"Error: {exc.message} :: Status: {exc.status_code}", exc_info=exc)
    return JSONResponse(status_code=exc.status_code, content={"status": "error",
                                                              "data": f"{datetime.now()}",
                                                              "detail": exc.message})


@main_app.exception_handler(Exception)
async def default_exception(request: Request, exc: Exception) -> JSONResponse:
    logger.error(msg=f"Error: {exc} :: Status: {status.HTTP_500_INTERNAL_SERVER_ERROR}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": "error",
                 "data": f"{datetime.now()}",
                 "details": "Что-то пошло не так, попробуйте позже"},
    )


main_app.include_router(router_v1, prefix="/api/v1")
main_app.add_middleware(SessionMiddleware, secret_key=settings.auth_google.SECRET_KEY_FOR_SESSION)

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
