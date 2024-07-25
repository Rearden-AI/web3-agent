from discord import Intents

from .classes.rearden_discord_client import ReardenDiscordClient
from .classes.discord_settings import DiscordSettings

intents = Intents.default()
intents.message_content = True

rearden_discord_client = ReardenDiscordClient(intents=intents)


async def run_discord_bot():
    await rearden_discord_client.start(DiscordSettings().DISCORD_BOT_AUTH)
