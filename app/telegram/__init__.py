import telegram

from .config import TelegramConfig

tg_config = TelegramConfig()

bot = telegram.Bot(token=tg_config.TG_TOKEN)

async def notify(msg: str, chat_id=tg_config.TG_CHAT_ID):
    if len(msg) > 4096:
        for x in range(0, len(msg), 4096):
            await bot.send_message(chat_id, msg[x:x+4096])
    else:
        await bot.send_message(chat_id, msg)

async def notify_error(msg):
    await notify(msg=msg, chat_id=tg_config.TG_ERROR_CHAT_ID)
    