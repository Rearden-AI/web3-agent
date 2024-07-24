from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from .vs_update import update_knowledge


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_knowledge, "cron", hour='*/1')
    scheduler.start()

    yield


vectorstore_updater_app = FastAPI(lifespan=lifespan)
