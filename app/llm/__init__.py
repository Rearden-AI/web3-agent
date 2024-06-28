import logging

from app.llm.modules.langgraph import process_user_message_flow
from .classes.llm_response import LlmResponse

logger = logging.getLogger('llm')

def process_user_message(
        message: str,
        chain_id: int,
        address: str
    ) -> LlmResponse:
    flow_result = process_user_message_flow(
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
