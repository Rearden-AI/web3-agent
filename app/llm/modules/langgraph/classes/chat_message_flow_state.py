from typing import Any
from typing_extensions import TypedDict


class ChatMessageFlowState(TypedDict):
    user_message: str
    message_category: str
    action_category: str
    action_processed_successfully: bool
    num_steps: int
    response: str
    actions: list[Any]
    user_address: str
    chooseable_actions: list = []
    chain_id: int
    