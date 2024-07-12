import logging

from discord import Client, Message

from app.llm import process_project_question

logger = logging.getLogger("Discord client")


class ReardenDiscordClient(Client):
    async def on_message(self, message: Message):
        if message.author.id == 1260903898030407703:
            return

        logger.debug(f"Received message: {message}")

        project = self.__get_project(message.channel.name)

        response = await process_project_question(
            message=message.content,
            project=project
        )
        await message.reply(response)

        # await message.channel.send(response)

    def __get_project(self, channel_name):
        if channel_name == "test-wormhole":
            return "wormhole"
