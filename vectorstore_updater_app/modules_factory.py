import redis

from .config import config, redis_config, tg_conf
from utils import knowledge_driver, telegram_bot

redis_db = redis.Redis(
    host=redis_config.REDIS_HOST,
    port=redis_config.REDIS_PORT,
    username=redis_config.REDIS_USER,
    password=redis_config.REDIS_PASSWORD,
    encoding="utf8"
)

# -------- Initialize knowledge driver ----------------
kd = knowledge_driver.KnowledgeDriver(discord_auth=config.DISCORD_AUTH)
# -------- Initialize Telegram Bot --------------------
tg_bot = telegram_bot.TelegramBot(token=tg_conf.TG_TOKEN, chat=tg_conf.TG_CHAT_ID)
