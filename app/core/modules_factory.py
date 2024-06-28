import redis
from web3 import Web3, HTTPProvider

from app.core.config import config, redis_config, tg_conf
from utils import knowledge_driver, telegram_bot

redis_db = redis.Redis(host=redis_config.REDIS_HOST, port=redis_config.REDIS_PORT)
web3 = Web3(HTTPProvider(config.WEB3_PROVIDER))

# -------- Initialize knowledge driver ----------------
kd = knowledge_driver.KnowledgeDriver()
# -------- Initialize Telegram Bot --------------------
tg_bot = telegram_bot.TelegramBot(token=tg_conf.TG_TOKEN, chat=tg_conf.TG_CHAT_ID)
