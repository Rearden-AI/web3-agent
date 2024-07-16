from pydantic_settings import BaseSettings


class TelegramConfig(BaseSettings):
    TG_TOKEN: str = ""
    TG_CHAT_ID: str = ""
    TG_ERROR_CHAT_ID: str = ""
    