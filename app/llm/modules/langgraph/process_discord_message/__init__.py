from langgraph.graph import END, StateGraph

from .classes.discord_message_flow_state import DiscordMessageFlowState
from .utils import get_initial_state

from ..process_chat_message.nodes import answer_based_on_documentation

workflow = StateGraph(DiscordMessageFlowState)

workflow.add_node('answer_based_on_documentation', answer_based_on_documentation)
workflow.set_entry_point('answer_based_on_documentation')
workflow.add_edge('answer_based_on_documentation', END)

app = workflow.compile()


async def process_discord_message_flow(
        user_message: str,
        project: str
):
    initial_state = get_initial_state(
        user_message,
        project
    )

    return await app.ainvoke(input=initial_state)
