from app.llm.modules.langgraph.classes.chat_message_flow_state import ChatMessageFlowState


def action_result_router(state: ChatMessageFlowState):
    return 'finish' if state['action_processed_successfully'] else 'docs'
