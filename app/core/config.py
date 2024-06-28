import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    APP_DOMAIN: str = "localhost"
    GOOGLE_API_KEY: str = ""
    WEB3_PROVIDER: str = "localhost"


class RedisSettings(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = ""
    REDIS_URL: str = f'redis://{REDIS_HOST}:{REDIS_PORT}'


class TelegramSettings(BaseSettings):
    TG_TOKEN: str = ""
    TG_CHAT_ID: str = ""

class OLLAMASettings(BaseSettings):
    OLLAMA_HOST: str = "localhost"
    OLLAMA_PORT: str = ""
    OLLAMA_URL: str = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"

class DBSettings(BaseSettings):
    DB_NAME: str = ""
    DB_USER: str = ""
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_PW: str = ""

    SQLALCHEMY_DATABASE_URL: str = f'postgresql+asyncpg://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    db_echo: bool = False


config = Config()
tg_conf = TelegramSettings()
db_config = DBSettings()
redis_config = RedisSettings()
ollama_config = OLLAMASettings()
