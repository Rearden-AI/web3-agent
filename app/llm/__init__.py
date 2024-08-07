import logging

from app.llm.modules.langgraph import process_user_message_flow, process_discord_message_flow
from .classes.llm_response import LlmResponse

logger = logging.getLogger('llm')


async def process_user_message(
        message: str,
        chain_id: int,
        address: str
    ) -> LlmResponse:
    flow_result = await process_user_message_flow(
        message=message,
        chain_id=chain_id,
        address=address)

    logger.info(flow_result)

    response = LlmResponse(
        text=flow_result['response'],
        actions=flow_result['actions'],
        chooseable_actions=flow_result['chooseable_actions']
    )

    return response


async def process_project_question(
        message: str,
        project: str
):
    flow_result = await process_discord_message_flow(message, project)
    return flow_result['response']
    