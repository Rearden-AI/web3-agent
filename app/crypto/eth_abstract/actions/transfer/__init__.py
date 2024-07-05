from .constants.abis import ERC_20_ABI
from ...enums.evm_chain import EvmChain
from ....classes.token import Token
from ....services.tokens_keeper import get_token_by_symbol
from ....constants.links import ETH_ICON_URL


def get_transfer_data_for_chain(symbol: str, receiver: str, amount: float, evm_chain: EvmChain, **params):
    token = get_token_by_symbol(symbol) if symbol != "ETH" else None

    transaction_data = __get_transaction_data(symbol, receiver, amount, token, evm_chain)

    return {
        "description": f"Transfer {symbol}",
        "type": "Transfer",
        "parameters_description": [
            {
                "name": "Token",
                "value": symbol,
                "icon": ETH_ICON_URL if symbol == "ETH" else token.icon_url
            }
        ],
        "transaction_data": transaction_data,
        "balance_data": {
            "coin": "native" if symbol == "ETH" else token.token_data[evm_chain].address
        }
    }


def __get_transaction_data(
        symbol: str,
        receiver: str,
        amount: float,
        token: Token,
        evm_chain: EvmChain):
    if symbol == "ETH":
        return __get_send_native_coin_transaction_data(receiver, amount)

    return __get_send_erc_20_token_transaction_data(
        receiver,
        amount,
        token,
        evm_chain
    )


def __get_send_native_coin_transaction_data(receiver: str, amount: float):
    inputs = []

    to = {"input_id": 0}
    inputs.append({
        "id": 0,
        "value_source": "user_input",
        "value": receiver,
        "description": "Enter receiver address",
        "type": "address"
    })

    value = {"input_id": 1}
    inputs.append({
        "id": 1,
        "value_source": "user_input",
        "value": amount,
        "description": "Enter ETH amount to send",
        "type": "amount",
        "decimals": 18,
        "symbol": "ETH",
        "icon_url": ETH_ICON_URL
    })

    return {
        "to": to,
        "value": value,
        "inputs": inputs
    }


def __get_send_erc_20_token_transaction_data(
        receiver: str,
        amount: float,
        token: Token,
        evm_chain: EvmChain
):
    method_params = []
    inputs = []

    method_params.append({"input_id": 0})
    inputs.append({
        "id": 0,
        "value_source": "user_input",
        "value": receiver,
        "description": "Enter receiver address",
        "type": "address"
    })

    method_params.append({"input_id": 1})
    inputs.append({
        "id": 1,
        "value_source": "user_input",
        "value": amount,
        "description": f"Enter {token.symbol} amount to send",
        "type": "amount",
        "decimals": token.token_data[evm_chain].decimals,
        "symbol": token.symbol,
        "icon_url": token.icon_url
    })

    return {
        "to": token.token_data[evm_chain].address,
        "method_name": "transfer",
        "method_params": method_params,
        "abis": {
            token.token_data[evm_chain].address: ERC_20_ABI
        },
        "inputs": inputs
    }
