from ..classes.chat_message_flow_state import ChatMessageFlowState


def categorize_user_message_router(state: ChatMessageFlowState):
    return state['message_category']
