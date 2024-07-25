import logging

from discord import Client, Message

from app.llm import process_project_question

logger = logging.getLogger("Discord client")


class ReardenDiscordClient(Client):
    async def on_message(self, message: Message):
        if message.author.name == "Rearden AI Helper":
            return

        logger.debug(f"Received message: {message}")
        logger.debug(f"Received message: {message.content}")

        project = self.__get_project(message.channel.name)

        response = await process_project_question(
            message=message.content, project=project
        )
        await message.reply(response)

    def __get_project(self, channel_name):
        if channel_name == "wormhole":
            return "wormhole"
