import logging

from ..classes.chat_message_flow_state import ChatMessageFlowState

logger = logging.getLogger('dummy')


def dummy(state: ChatMessageFlowState):
    logger.info(f"dummy: {state['message_category']}")

    num_steps = int(state['num_steps'])
    num_steps += 1

    return {'num_steps': num_steps, 'response': 'dummy'}
