from .classes import ChatMessageFlowState


def get_initial_state(
    message: str,
    chain_id: int,
    address: str
) -> ChatMessageFlowState:
    return ChatMessageFlowState(
        user_address=address,
        user_message=message,
        chain_id=chain_id,
        num_steps=0,
        actions=[],
        chooseable_actions=[]
    )
