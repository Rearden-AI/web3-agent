from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DISCORD_AUTH: str = ""


class RedisSettings(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = ""
    REDIS_USER: str = ""
    REDIS_PASSWORD: str = ""
    REDIS_URL: str = f'redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}'


class TelegramSettings(BaseSettings):
    TG_TOKEN: str = ""
    TG_CHAT_ID: str = ""


class ChromaSettings(BaseSettings):
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8000


config = Config()
tg_conf = TelegramSettings()
redis_config = RedisSettings()
chroma_settings = ChromaSettings()
