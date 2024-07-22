import requests
import json 
import logging

import asyncio


from typing_extensions import TypedDict
from typing import Any

from langgraph.graph import END, StateGraph
from langchain_community.llms import Ollama

from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from discord import Client, Message, Intents


def get_transaction_info(tx: str):


    res = requests.get(f'https://api.wormholescan.io/api/v1/operations?txHash={tx}')
    response = json.loads(res.text)
    return response

def parse_result(operations):
    print(operations)

    if "operations" not in operations:
        return False

    found = len(operations["operations"]) > 0

    if not found:
        return False
    
    operation = operations["operations"][0]

    tokens_redeemed = "targetChain" in operation

    return {
        "tokens_redeemed": tokens_redeemed
    }

class TransactionStatus(TypedDict):
    tokens_redeemed: bool

class CheckTransactionFlowState(TypedDict):
    user_message: str
    tx_hashes: list[str]
    tx_status: bool | TransactionStatus
    response: str

workflow = StateGraph(CheckTransactionFlowState)

model = Ollama(model='llama3')

find_tx_hash_template_msg = """You are master in finding blockchain transaction hash in user messages.
If user indicates transaction hash in USER_MESSAGE output ONLY this hash, e.g.: 8cc97eeebef84a78770c9b74127880a68bafd8e37b7cefdc79b3756996d4de1a
If you find several transactions in USER_MESSAGE output them all separated by a space.
If you cannot find hash in USER_MESSAGE, output 'not_found'

USER_MESSAGE:
{user_message}
"""

find_tx_hash_template = PromptTemplate(
    template=find_tx_hash_template_msg,
    input_variables=["user_message"]
)

find_tx_hash_chain = (
    {
        "user_message": RunnablePassthrough()
    }
    | find_tx_hash_template
    | model
    | StrOutputParser()
)


def find_tx_hashes_in_message(state: CheckTransactionFlowState):
    user_message = state['user_message']
    print()
    print("find_tx_hashes_in_message")
    print(f"Searching for tx hashes in {user_message}")

    result = find_tx_hash_chain.invoke(user_message)

    tx_hashes = []

    if result == "not_found":
        pass
    else:
        tx_hashes = result.split()

    print(f"Found {tx_hashes}")

    return {"tx_hashes": tx_hashes}

workflow.add_node("find_tx_hashes_in_message", find_tx_hashes_in_message)

def ask_for_tx_hash(state: CheckTransactionFlowState):
    print()
    print("ask_for_tx_hash")
    print('Asking for a messae with valid tx hashes')

    response = model.invoke("User has not provided any valid tx hash. Ask user to provide wormhole transaction hash")

    return {"response": response}

workflow.add_node("ask_for_tx_hash", ask_for_tx_hash)

def check_transactions(state: CheckTransactionFlowState):
    print()
    print("checking transactions")

    for tx_hash in state['tx_hashes']:
        tx_status = parse_result(get_transaction_info(tx_hash))
        if tx_status:
            print("found transaction result")
            return {"tx_status": tx_status}

    print("Not found transaction result")
        
    return {"tx_status": False}

workflow.add_node("check_transactions", check_transactions)

interpret_tx_result_tmpl_msg = """You are master in interpreting transaction result.
If tokens were redeemed advise to bridge tokens back.
If tokens were not redemeed tell that and advise to redeem tokens.

Tokens were redeemed: {tokens_redeemed}
"""

interpret_tx_result_tmpl = PromptTemplate(
    template=interpret_tx_result_tmpl_msg,
    input_variables=["tokens_redeemed"]
)

def tokens_were_redeemed(tokens_redeemed):
    print()
    print("tokens_were_redeemed")
    print(tokens_redeemed)
    return "yes" if tokens_redeemed["tokens_redeemed"] else "no" 

interpret_tx_result_chain = (
    {
        "tokens_redeemed": tokens_were_redeemed
    }
    | interpret_tx_result_tmpl
    | model
    | StrOutputParser()
)


def interpret_tx_result(state: CheckTransactionFlowState):
    print()
    print("interpret_tx_result")
    print(f"Interprenting transaction result: {state['tx_status']}")

    result = interpret_tx_result_chain.invoke(state['tx_status'])

    return {"response": result}

workflow.add_node("interpret_tx_result", interpret_tx_result)

workflow.set_entry_point("find_tx_hashes_in_message")

def transactions_fount_count_router(state: CheckTransactionFlowState):
    return "None" if len(state["tx_hashes"]) == 0 else "Found"

workflow.add_conditional_edges(
    "find_tx_hashes_in_message",
    transactions_fount_count_router,
    {
        "None": "ask_for_tx_hash",
        "Found": "check_transactions"
    }
)

workflow.add_edge("ask_for_tx_hash", END)

def check_transactions_router(state: CheckTransactionFlowState):
    return "Found" if state["tx_status"] else "None"

workflow.add_conditional_edges(
    "check_transactions",
    check_transactions_router,
    {
        "Found": "interpret_tx_result",
        "None": "ask_for_tx_hash"
    }
)

workflow.add_edge("interpret_tx_result", END)
app = workflow.compile()


logger = logging.getLogger("Discord client")


intents = Intents.default()
intents.typing = True
intents.messages = True
intents.message_content = True

rearden_discord_client = Client(intents=intents)

@rearden_discord_client.event
async def on_message(message: Message):
    if message.author.id == 1260903898030407703:
        return

    print(f"Received message: {message}")
    print(f'Author: {message.author.name}')
    print(f'Content: {message.content}')
    print(f'Clean_Content: {message.clean_content}')
    print(f'System_Content: {message.system_content}')


    
    response = app.invoke({"user_message": message.content})
    print()
    print("RESPONSE")
    print(response)
    await message.reply(response["response"])

asyncio.run(rearden_discord_client.run(""))