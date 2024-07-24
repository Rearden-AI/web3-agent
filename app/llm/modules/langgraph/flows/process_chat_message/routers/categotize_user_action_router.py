from ..classes import ChatMessageFlowState


def categotize_user_action_router(state: ChatMessageFlowState):
    return state['action_category'] \
        if state['action_category'] in ['transfer', 'swap', 'invest'] else \
            'off_topic'
