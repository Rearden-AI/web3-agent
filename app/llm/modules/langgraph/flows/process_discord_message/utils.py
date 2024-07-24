from .classes.discord_message_flow_state import DiscordMessageFlowState


def get_initial_state(
        user_message: str,
        project: str
) -> DiscordMessageFlowState:
    return DiscordMessageFlowState(
        user_message=user_message,
        project=project,
        num_steps=0
    )
