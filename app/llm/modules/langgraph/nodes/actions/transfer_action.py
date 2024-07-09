import logging

from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser

from app.crypto import get_transaction_data
from app.crypto.services.tokens_keeper import get_tokens

from app.llm.utils import *
from app.llm.modules.llm import get_model
from ...classes import ChatMessageFlowState

logger = logging.getLogger("transfer_action")

tokens = get_tokens()
tokens_list = '\n'.join(map(lambda x: f"{x.name} ({x.symbol})", tokens)) + "\nEthereum (ETH)"

system_message_template = """
You are an expert in recognizing what token user wants to transfer.

Here is a list of accepted tokens in format "name (symbol)"

TOKENS_LIST:
{{ tokens_list }}

Analyze user message from USER_MESSAGE and response with pure JSON with three keywords: 'symbol', 'amount' and 'receiver'

'symbol' - is symbol from TOKENS_LIST.
'amount' - is amount of tokens to transfer. Set to null if not defined.
'receiver' - is a wallet to receive tokens. Set to null if not defined.

DO NOT include any comments in response.
"""

prefix = get_prefix_template(system_message=system_message_template)

few_shot_template = FewShotPromptTemplate(
    prefix=prefix,
    template_format="jinja2",
    example_prompt=PromptTemplate(
        template=get_few_shot_template(),
        input_variables=["user_message", "assistant_message"],
        template_format="jinja2"
    ),
    examples=[
        {
            "user_message": "I want to send some USDT",
            "assistant_message": """{
"symbol": "ETH",
"amount": null,
"receiver": null
}"""
        },
        {
            "user_message": "I want to send some Ether to 0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97",
            "assistant_message": """{
"symbol": "ETH",
"amount": null,
"receiver": "0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97"
}"""
        },
        {   
            "user_message": "I want to send 10 USDC to 0x302166D919016E9927b2610dB95C756343B93623",
            "assistant_message": """{
"symbol": "USDC",
"amount": 10,
"receiver": "0x302166D919016E9927b2610dB95C756343B93623"
}"""
        }
    ],
    suffix=get_suffix_template(),
    input_variables=["tokens_list", "user_message"]
)

model = get_model()

test_chain = ({
        "tokens_list": lambda _: tokens_list,
        "user_message": RunnablePassthrough()
    }
    | few_shot_template
)

chain = (
    {
        "tokens_list": lambda _: tokens_list,
        "user_message": RunnablePassthrough()
    }
    | few_shot_template
    | model
    | JsonOutputParser()
)


async def transfer_action(state: ChatMessageFlowState):
    logger.info('Processing transfer action')

    user_message = state['user_message']
    num_steps = int(state['num_steps'])
    num_steps += 1

    try:
        transfer_params = await chain.ainvoke(user_message)
        
        action_data = get_transaction_data(
            chain_id=state["chain_id"],
            data={
                "action": "transfer",
                "params": transfer_params
            }
        )

        return {
            "num_steps": num_steps, 
            "response": 'Processing transfer action', 
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
