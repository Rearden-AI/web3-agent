import telegram

from .config import TelegramConfig

tg_config = TelegramConfig()

bot = telegram.Bot(token=tg_config.TG_TOKEN)

async def notify(msg: str, chat_id=tg_config.TG_CHAT_ID):
    await bot.send_message(chat_id=chat_id, text=msg)

async def notify_error(msg):
    await notify(msg=msg, chat_id=tg_config.TG_ERROR_CHAT_ID)
    