from typing_extensions import TypedDict


class DiscordMessageFlowState(TypedDict):
    user_message: str
    num_steps: int
    project: str
    response: str
