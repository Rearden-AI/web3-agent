# pylint: disable=wrong-import-position
import logging

from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse, PlainTextResponse
import redis.asyncio as redis
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from apscheduler.schedulers.background import BackgroundScheduler

from app.logging_config import configure_logging
configure_logging()

# this is needed for alempic migrations
from app.core.models import db_helper, Base

from app.api import router as router_v1
from app.core.config import config, redis_config
from app.llm.modules.langgraph.nodes.answer_based_on_documentation import update_knowledge
from app import telegram

from utils.extra import check_transactions_status

logger = logging.getLogger("app")


# from fastapi_pagination import add_pagination

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    # scheduler.add_job(check_transactions_status, "cron", second='*/30')
    scheduler.add_job(update_knowledge, "cron", hour='*/23')
    scheduler.start()
    redis_connection = redis.from_url(redis_config.REDIS_URL, encoding="utf8")

    # await llm_driver.initialize()

    print("Started lifespan")
    await FastAPILimiter.init(redis_connection)
    yield
    await FastAPILimiter.close()
    print("End lifespan")


app = FastAPI(lifespan=lifespan)

allow_origins = [config.APP_DOMAIN]
if config.DEV_DOMAIN:
    allow_origins.append(config.DEV_DOMAIN)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router=router_v1, prefix=config.api_v1_prefix)

@app.exception_handler(HTTPException)
async def exception_handler(request: Request, exc: HTTPException):
    msg = (await format_request(request)) + "\n\n" + str(exc)

    await telegram.notify_error(msg)
    return await http_exception_handler(request, exc)


async def set_body(request: Request, body: bytes):
    async def receive():
        return {"type": "http.request", "body": body}

    request._receive = receive


async def get_body(request: Request) -> bytes:
    body = await request.body()
    await set_body(request, body)
    return body


@app.middleware("http")
async def errors_handling(request: Request, call_next):
    body = await request.body()
    try:
        await set_body(request, body)
        return await call_next(request)
    except Exception as exc:
        msg = f"URL: {request.url}\n"
        msg += f"Body: {body.decode()}"
        msg += "\n\n"
        msg += str(exc)

        await telegram.notify_error(msg)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=str(exc)
        )



async def format_request(request: Request):
    msg = f"URL: {request.url}\n"

    body = await request.body()
    msg += f"Body: {body.decode()}"

    return msg

# add_pagination(app)
