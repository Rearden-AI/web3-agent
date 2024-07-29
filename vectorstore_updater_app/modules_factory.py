import logging

from .config import config, tg_conf
from utils import knowledge_driver, telegram_bot

# -------- Initialize knowledge driver ----------------
kd = knowledge_driver.KnowledgeDriver(discord_auth=config.DISCORD_AUTH)
logging.getLogger("initialized").info(f"disco token:{config.DISCORD_AUTH}")
# -------- Initialize Telegram Bot --------------------
tg_bot = telegram_bot.TelegramBot(token=tg_conf.TG_TOKEN, chat=tg_conf.TG_CHAT_ID)
