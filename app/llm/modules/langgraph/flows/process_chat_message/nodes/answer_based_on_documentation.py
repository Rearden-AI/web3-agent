from app.llm.modules.langgraph.common_chains.documentation_rag import (
    find_answer_in_documentation,
)
from app.llm.modules.langgraph.flows.process_chat_message.classes.chat_message_flow_state import (
    ChatMessageFlowState,
)


async def answer_based_on_documentation(state: ChatMessageFlowState):
    # logger.info("Searching in documentation...")

    user_message = state["user_message"]
    num_steps = int(state["num_steps"])
    num_steps += 1

    llm_response = await find_answer_in_documentation(user_message)

    return {"num_steps": num_steps, "response": llm_response}
