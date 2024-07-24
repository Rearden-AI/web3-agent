from discord import Intents

from .classes.rearden_discord_client import ReardenDiscordClient
from .classes.discord_settings import DiscordSettings

intents = Intents.default()
intents.message_content = True

rearden_discord_client = ReardenDiscordClient(intents=intents)


def run_discord_bot():
    rearden_discord_client.run(DiscordSettings().DISCORD_BOT_AUTH)
