from ..classes import ChatMessageFlowState


def action_result_router(state: ChatMessageFlowState):
    return 'finish' if state['action_processed_successfully'] else 'docs'
