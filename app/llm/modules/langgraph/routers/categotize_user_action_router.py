from app.llm.modules.langgraph.classes.chat_message_flow_state import ChatMessageFlowState


def categotize_user_action_router(state: ChatMessageFlowState):
    return state['action_category']