import logging

from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser

from app import crypto
from app.crypto.services.tokens_keeper import get_tokens
from app.llm.modules.llm import get_model
from app.llm.utils import *
from ...classes import ChatMessageFlowState

logger = logging.getLogger("swap_action")

system_message_template = """
You are an expert in recognizing what token user wants to trade.

Here is a list of accepted tokens in format "name (symbol)"
{{ tokens_list }}

Analyze user message from USER_MESSAGE and return JSON with two keywords: 'symbol' and 'side'.
'symbol' - is symbol from list.
'side' is 'buy' if user wants to buy tokens and 'sell' if user want to sell tokens.

Return empty object if you can't recognize values.
"""

template = get_template(system_message=system_message_template)

prompt_template = PromptTemplate(
    template=template,
    input_variables=["tokens_list", "user_message"],
    template_format="jinja2"
)

model = get_model()

chain = (
    prompt_template
    | model
    | JsonOutputParser()
)

def swap_action(state: ChatMessageFlowState):
    logger.info('Processing swap action')

    num_steps = int(state['num_steps'])
    num_steps += 1

    user_message = state['user_message']

    chain_id=state["chain_id"]

    tokens = get_tokens()
    tokens_list = '\n'.join(map(lambda x: f"{x.name} ({x.symbol})", tokens))

    try:
        swap_params = chain.invoke({
            "tokens_list": tokens_list,
            "user_message": user_message
        })

        action_data = crypto.get_transaction_data(
            chain_id=chain_id,
            data={
                "action": "swap",
                "params": {
                    "side": swap_params["side"],
                    "symbol": swap_params["symbol"],
                    "user_address": state["user_address"]
                }
            }
        )

        return {
            "num_steps": num_steps,
            "response": "Processing swap action...",
            "action_processed_successfully": True,
            "actions": [
                {
                    "id": 0,
                    "action_data": action_data
                }
            ]
        }
    except:
        return {
            "num_steps": num_steps,
            "action_processed_successfully": False
        }
