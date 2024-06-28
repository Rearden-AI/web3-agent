from langgraph.graph import END, StateGraph

from app.llm.utils import get_initial_state

from .routers import categotize_user_action_router
from .routers import categorize_user_message_router

from .nodes import categorize_user_request
from .nodes import answer_based_on_documentation
from .nodes import dummy
from .nodes import categorize_user_action

from .nodes.actions import swap_action
from .nodes.actions import invest_action
from .nodes.actions import transfer_action

from .classes import ChatMessageFlowState

workflow = StateGraph(ChatMessageFlowState)

workflow.add_node('categorize_user_request', categorize_user_request)
workflow.add_node('answer_based_on_documentation', answer_based_on_documentation)
workflow.add_node('categorize_user_action', categorize_user_action)
# workflow.add_node('dummy', dummy)

workflow.add_node('swap_action', swap_action)
workflow.add_node('invest_action', invest_action)
workflow.add_node('transfer_action', transfer_action)

workflow.add_conditional_edges(
    'categorize_user_request',
    categorize_user_message_router,
        {
            'execute_action': 'categorize_user_action',
            'ask_for_data': 'answer_based_on_documentation',
            'off_topic': 'answer_based_on_documentation'
        }
    )

workflow.add_conditional_edges(
    'categorize_user_action',
    categotize_user_action_router,
    {
        'transfer': 'transfer_action',
        'swap': 'swap_action',
        'invest': 'invest_action'
    }
)

workflow.set_entry_point('categorize_user_request')

workflow.add_edge('answer_based_on_documentation', END)
# workflow.add_edge('execute_action', END)
# workflow.add_edge('dummy', END)

workflow.add_edge('swap_action', END)
workflow.add_edge('invest_action', END)
workflow.add_edge('transfer_action', END)

app = workflow.compile()


def process_user_message_flow(
        message: str,
        chain_id: int,
        address: str
    ) -> ChatMessageFlowState:
    initial_state = get_initial_state(
        message=message,
        chain_id=chain_id,
        address=address
    )

    return app.invoke(input=initial_state)