import asyncio
import datetime
import json
import logging
import re
import uuid
from dataclasses import dataclass
from typing import Annotated
import jsonpickle

from app.core.models.user import User
from app.llm import process_user_message
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import dependencies as auth_dependencies
from app.core.errors import errors
from app.core.models import db_helper, Chat
from app.core.modules_factory import redis_db
from .strategies import build_strategy
from .. import crud
from ..schemas import ChatResponse, ExtendedChatSchema, DataIn
from ...transactions.crud import get_by_id as get_tx_by_id

from app.crypto.eth.investments import investment_actions as investment_actions_eth
from app.crypto.eth_holesky.investments import investment_actions as investment_actions_holesky
from app.crypto.services.tokens_keeper import get_token_by_symbol

from app.core.config import superadmin_settings


async def get_chat_by_id(
        chat_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Chat:
    chat = await crud.select_by_id(session=session, chat_id=chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=errors.chats.PROJECT_NOT_FOUND
        )

    return chat


async def get_chat_by_uuid(
        chat_uuid: Annotated[str, Path],
        user: User = Depends(auth_dependencies.extract_user_from_access_token),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Chat:
    chat = await crud.select_by_uuid(session=session, chat_uuid=chat_uuid)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            # detail=errors.chats.PROJECT_NOT_FOUND
        )

    if user.wallet != superadmin_settings.SUPERADMIN_WALLET_ADDRESS and chat.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            # detail=errors.chats.USER_NOT_OWNER
        )

    return chat


async def get_extended_chat_by_uuid(
        chat_uuid: Annotated[str, Path],
        user=Depends(auth_dependencies.extract_user_from_access_token),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> ExtendedChatSchema:
    chat = await get_chat_by_uuid(chat_uuid, user, session)

    chat = ExtendedChatSchema.from_orm(chat)
    history = redis_db.get(chat.uuid)
    if history:
        chat.history = json.loads(history)
    else:
        chat.history = []

    return chat


@dataclass
class ChatContext:
    current_input: str
    current_dt: datetime.datetime
    history: list[dict]
    minimized_history: list[dict]
    chat_id: str


async def process_chat_request(
        data_in: DataIn,
        chat: ExtendedChatSchema = Depends(get_extended_chat_by_uuid),
        user: User = Depends(auth_dependencies.extract_user_from_access_token),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> ChatResponse:
    if not data_in.generate_code:
        data_in.generate_code = []
    context = ChatContext(
        current_input=data_in.message,
        current_dt=datetime.datetime.now(),
        history=chat.history,
        minimized_history=_init_chatbot_history_context(chat),
        chat_id=chat.uuid
    )
    if not data_in.message and not data_in.generate_code and not data_in.transaction_ids and not data_in.chosen_action_key:
        raise HTTPException(
            detail="No needed data received",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if data_in.generate_code:
        timestamp=int(datetime.datetime.now().timestamp() * 1000)
        chat.history.append(
            {
                "role": "model",
                "content": "", 
                "strategies": ['sui'],
                "timestamp": timestamp
            })
        
        res = ChatResponse(
            exec_logs="",
            body="",
            strategies=["sui"],
            contains_strategy_previews=[""],
            transactions=[],
            timestamp=timestamp
        )
    elif data_in.chosen_action_key:
        print('here')

        timestamp=int(datetime.datetime.now().timestamp() * 1000)

        if data_in.chain_id == 1:
            actions = investment_actions_eth[data_in.chosen_action_key]
        else:
            actions = investment_actions_holesky[data_in.chosen_action_key]
            
        print(actions)

        res = ChatResponse(
            body="",
            actions=actions,
            timestamp=timestamp
        )

        chat.history.append({
                "role": "model",
                "content": "",
                "actions": actions,
                "timestamp": timestamp
        })
    elif data_in.transaction_ids:
        timestamp=int(datetime.datetime.now().timestamp() * 1000)
        transactions = []
        for tx_id in data_in.transaction_ids:
            tx_from_db = await get_tx_by_id(session, tx_id)
            tx = {
                'id': tx_from_db.id,
                'amount': tx_from_db.amount,
                'token_symbol': tx_from_db.token_symbol,
                'token_icon': __get_token_icon(tx_from_db.token_symbol),
                'transaction_type': tx_from_db.transaction_type,
                'status': tx_from_db.status.value, 
                'transaction_hash': tx_from_db.transaction_hash,
                'transaction_on_explorer': __get_tx_on_explorer(tx_from_db.transaction_hash, tx_from_db.network),
                'to_address': tx_from_db.to_address,
                'from_address': tx_from_db.from_address,
                'chat_uuid': tx_from_db.chat_uuid,
                'action_name': tx_from_db.action_name,
                'network': tx_from_db.network,
                'timestamp': tx_from_db.timestamp
            }
            transactions.append(tx)

        chat.history.append(
            {
                "role": "model",
                "content": "",
                "transactions": transactions,
                "timestamp": timestamp
            }
        )
        res = ChatResponse(
            exec_logs="",
            body="",
            transactions=transactions,
            timestamp=timestamp,
            strategies=[],
            contains_strategy_previews=[]
        )
    else:
        _user_message = {"role": "user", "content": data_in.message, "parts": [data_in.message], "timestamp": data_in.timestamp}
        chat.history.append(_user_message)

        llm_response = process_user_message(
            message=data_in.message,
            chain_id=data_in.chain_id,
            address=user.wallet
        )

        timestamp=int(datetime.datetime.now().timestamp() * 1000)
        res = ChatResponse(
            exec_logs="",
            body=llm_response.text,
            actions=llm_response.actions,
            chooseable_actions=llm_response.chooseable_actions,
            transactions=[],
            timestamp=timestamp
        )

        chat.history.append({
                "role": "system",
                "content": llm_response.text,
                "parts": [llm_response.text],
                "timestamp": timestamp,
                "actions": llm_response.actions,
                "chooseable_actions": list(map(lambda action: {
                    "name": action.name,
                    "key": action.key,
                    "approxApy": action.approxApy
                }, llm_response.chooseable_actions)),
            })


    redis_db.set(chat.uuid, jsonpickle.encode(chat.history))

    return res

    if data_in.generate_code:
        strategies = await build_strategy(data_in.generate_code)
        chat.history.append(
            {"role": "model", "content": "", "strategies": strategies})
        res = ChatResponse(
            exec_logs="",
            body="",
            strategies=strategies,
            contains_strategy_previews=data_in.generate_code
        )
    elif data_in.transaction_ids:
        transactions = []
        for tx_id in data_in.transaction_ids:
            tx = await get_tx_by_id(session, tx_id)
            transactions.append(tx)

        chat.history.append(
            {"role": "model", "content": "", "transactions": transactions}
        )
        res = ChatResponse(
            exec_logs="",
            body="",
            transactions=transactions
        )
    else:
        _user_message = {"role": "user", "content": data_in.message, "parts": [data_in.message]}
        context.minimized_history.append({"role": "user", "content": data_in.message})
        chat.history.append(_user_message)

        valid_strategy_preview_actions = ["deposit_steth_eigenlayer", "deposit_eth_lido"]
        target_history_context = context.minimized_history[-5:]

        try:
            text = await llm_driver.generate_llm_static_response(target_history_context)
        except Exception as err:
            logging.error(err)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=errors.chats.GOOGLE_API_RESOURCE_EXHAUSTED
            )

        output, contains_strategy_previews = _process_generated_output(text)

        contains_strategy_previews_fixed = []
        for strategy in contains_strategy_previews:
            for valid_strategy in valid_strategy_preview_actions:
                if valid_strategy in strategy:
                    contains_strategy_previews_fixed.append(valid_strategy)

        for valid_strategy in valid_strategy_preview_actions:
            if valid_strategy in output and valid_strategy not in contains_strategy_previews_fixed:
                contains_strategy_previews_fixed.append(valid_strategy)

        if not chat.name:
            chat_orm = await crud.select_by_id(session=session, chat_id=chat.id)
            chat_orm.name = output[:30]
            chat.name = output[:30]
            await session.commit()

        res = ChatResponse(
            exec_logs="",
            body=output,
            strategies=[],
            contains_strategy_previews=contains_strategy_previews_fixed
        )

        if text:
            chat.history.append({
                "role": "system",
                "content": output,
                "parts": [output],
                "contains_strategy_previews": contains_strategy_previews
            })

        logging.debug(f"Saving chat history: {chat.history}")

    redis_db.set(chat.uuid, json.dumps(chat.history))

    return res


request_actions = {
    "askUserAddress()": "askUserAddress()",
    "askTransactionAmount()": "askTransactionAmount()",
}


async def _generate_end_strategies(text: str):
    err = None
    strategies = []
    matches = extract_strategy_matches(text)
    for match in matches:
        print("Found block:", match)
        try:
            strategy = await build_strategy(input_text=match)
            logging.debug(f"Changed text: {text}")
            strategies.append(strategy)
        except NameError as e:
            err = e
            break
        except Exception as e:
            err = e
            continue

        for s_part in strategy:
            _s_uuid = str(uuid.uuid4())
            s_part["uuid"] = _s_uuid
            redis_db.set(f"tr_{_s_uuid}", json.dumps(s_part))

    if err: logging.error(err)
    return strategies


def _init_chatbot_history_context(chat):
    """Minimizes redis-stored history for bot requests."""
    chat_history_context = []
    for message_dict in chat.history:
        chat_history_context.append({"role": message_dict["role"], "content": message_dict["content"]})
    return chat_history_context


async def chat_to_redis():
    ...


async def chat_from_redis():
    ...


async def start_new_chat(
        user=Depends(auth_dependencies.extract_user_from_access_token),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    chat = await crud.create(session=session, user_id=user.id)
    redis_db.set(chat.uuid, json.dumps([]))

    return chat


def extract_strategy_matches(text: str):
    logging.debug(f"Extracting strategy matches for text: {text}")

    pattern = r'```python(.*?)```'
    # Find all matches with DOTALL to include newlines in the '.*?' match
    matches = re.findall(pattern, text, flags=re.DOTALL)
    if matches:
        logging.debug(f"Found matches on first filter: {matches}")
        return matches
    pattern = r'```(.*?)```'
    # Find all matches with DOTALL to include newlines in the '.*?' match
    matches = re.findall(pattern, text, flags=re.DOTALL)
    if matches:
        logging.debug(f"Found matches on second filter: {matches}")
        return matches

    logging.debug("No matches found")
    return []


def _process_generated_output(text: str):
    t_blocks = text.split("{-==-}")
    if len(t_blocks) == 1:
        return text, []
    if len(t_blocks) > 1:
        output = t_blocks[0]
        contains_strategy_previews = t_blocks[1].split(",")
        contains_strategy_previews = [x.strip() for x in contains_strategy_previews]

        return output, contains_strategy_previews


def __get_tx_on_explorer(hash, network):
    if network == "Mainnet":
        return f"https://etherscan.io/tx/{hash}"
    elif network == "Holesky":
        return f"https://holesky.etherscan.io/tx/{hash}"
    

def __get_token_icon(symbol):
    if symbol == "ETH":
        return "https://cdn.coinranking.com/rk4RKHOuW/eth.svg"
    return get_token_by_symbol(symbol=symbol).icon_url


async def main():
    text = "```python\nunsigned_transactions = []\ntmp = deposit_eth_lido(sender_address='0xF2B016466A8e9CFEFA7854b218535017192008E9', value=0.2)\nunsigned_transactions.extend(tmp)\ntmp = deposit_steth_eigenlayer(sender_address='0xF2B016466A8e9CFEFA7854b218535017192008E9', value=0.2)\nunsigned_transactions.extend(tmp)\n```"
    strategy = []
    matches = extract_strategy_matches(text)
    print(matches)
    if "+=" in text:
        try:
            strategy = await build_strategy(input_text=text)
            debug = text
            text = "Here is the strategy you've requested."
        except NameError as e:
            logging.debug(e)
            text = "Please, provide your wallet address to proceed"
        except Exception as e:
            text = f"Something went wrong during strategy build. {e}"
    print(strategy)


if __name__ == "__main__":
    asyncio.run(main())
