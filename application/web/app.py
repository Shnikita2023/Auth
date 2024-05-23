import logging
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from application.exceptions import ApplicationException
from application.web.views import router as router_v1

app = FastAPI(openapi_url="/api/v1/auth/openapi.json",
              version="1.1.1",
              title="Auth",
              docs_url="/api/v1/auth/docs",
              debug=True)

logger = logging.getLogger(__name__)


@app.exception_handler(ApplicationException)
async def application_exception_handler(request: Request, exc: ApplicationException):
    logger.error(msg=f"Error: {exc.message} :: Status: {exc.status_code}", exc_info=exc)
    return JSONResponse(status_code=exc.status_code, content={"status": "error",
                                                              "data": f"{datetime.now()}",
                                                              "detail": exc.message})

app.include_router(router_v1, prefix="/api/v1")

app.add_middleware(
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
