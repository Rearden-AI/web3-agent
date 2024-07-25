from pydantic_settings import BaseSettings


class DiscordSettings(BaseSettings):
    DISCORD_BOT_AUTH: str = ""
