# pylint: disable=wrong-import-position
from contextlib import asynccontextmanager
import redis.asyncio as redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from apscheduler.schedulers.background import BackgroundScheduler

from app.logging_config import configure_logging
configure_logging()

from app.api import router as router_v1
from app.core.config import config, redis_config
from app.llm.modules.langgraph.nodes.answer_based_on_documentation import update_knowledge
from utils.extra import check_transactions_status


# from fastapi_pagination import add_pagination

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_transactions_status, "cron", second='*/30')
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router=router_v1, prefix=config.api_v1_prefix)

# add_pagination(app)
