from discord import Intents

from .classes.rearden_discord_client import ReardenDiscordClient

rearden_discord_client = ReardenDiscordClient(intents=Intents.default())
