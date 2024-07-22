from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from app.logging_config import configure_logging
from app.llm.modules.langgraph.nodes.answer_based_on_documentation import update_knowledge

configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_knowledge, "cron", hour='*/23')
    scheduler.start()

    yield


app = FastAPI(lifespan=lifespan)
