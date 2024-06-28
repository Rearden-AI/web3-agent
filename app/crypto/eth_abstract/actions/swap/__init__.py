from .configs.swap_config import SwapConfig
from .constants.abis import UNISWAP_V2_ROUTER_ABI
from ...enums.evm_chain import EvmChain
from ....services.tokens_keeper import get_token_by_symbol
from ....constants.links import ETH_ICON_URL


def get_swap_data_for_chain(
        side: str,
        symbol: str,
        user_address: str,
        evm_chain: EvmChain,
        method_config: SwapConfig
    ):
    description = f'{"Buy" if side == "buy" else "Sell"} {symbol}'

    token = get_token_by_symbol(symbol)

    token_address = token.token_data[evm_chain].address
    decimals = token.token_data[evm_chain].decimals
    icon_url = token.icon_url

    method_name = "swapETHForExactTokens" if side == "buy" else "swapExactTokensForETH"
    method_params = __get_buy_method_params(
        token_address=token_address,
        user_address=user_address,
        swap_config=method_config) \
            if side == "buy" else \
                __get_sell_method_params(
                    token_address=token_address,
                    user_address=user_address,
                    swap_config=method_config)

    value = {"input_id": 2} if side == "buy" else None

    inputs = __get_buy_inputs(
        symbol=symbol,
        icon_url=icon_url,
        token_address=token_address,
        decimals=decimals,
        swap_config=method_config) \
            if side == "buy" else \
                __get_sell_inputs(
                    symbol=symbol,
                    icon_url=icon_url,
                    token_address=token_address,
                    decimals=decimals,
                    swap_config=method_config)

    uniswap_router_address = method_config.uniswap_v2_router_address

    parameters_description = [
            {
                "name": "From",
                "value": ("ETH" if side == "buy" else symbol),
                "icon": ETH_ICON_URL if side == "buy" else icon_url
            },
            {
                "name": "To",
                "value": ("ETH" if side == "sell" else symbol),
                "icon": ETH_ICON_URL if side == "sell" else icon_url
            }
        ]

    transaction_data = {
            "to": uniswap_router_address,
            "method_name": method_name,
            "method_params": method_params,
            "value": value,
            "abis": {
                uniswap_router_address: UNISWAP_V2_ROUTER_ABI
            },
            "inputs": inputs
        }

    return {
        "application_data": method_config.application_data,
        "description": description,
        "type": "Swap",
        "parameters_description": parameters_description,
        "transaction_data": transaction_data,
        "balance_data": {
            "coin": ("native" if side == "buy" else token_address),
            "symbol": ("ETH" if side == "buy" else symbol),
        }
    }


def __get_buy_method_params(
        token_address: str,
        user_address: str,
        swap_config: SwapConfig
):
    weth_address = swap_config.weth_address

    return [
        {
            "input_id": 0
        },
        [weth_address, token_address],
        user_address,
        {
            "input_id": 1
        }
    ]


def __get_sell_method_params(
        token_address: str,
        user_address: str,
        swap_config: SwapConfig
):
    weth_address = swap_config.weth_address
    return [
        {
            "input_id": 0
        },
        {
            "input_id": 1
        },
        [token_address, weth_address],
        user_address,
        {
            "input_id": 2
        }
    ]


def __get_sell_inputs(
        symbol: str,
        icon_url: str,
        decimals: int,
        token_address: str,
        swap_config: SwapConfig
):
    uniswap_router_address = swap_config.uniswap_v2_router_address
    weth_address = swap_config.weth_address

    return [
        {
            "id": 0,
            "value_source": "user_input",
            "description": f"Enter {symbol} amount",
            "type": "amount",
            "decimals": decimals,
            "symbol": symbol,
            "icon_url": icon_url
        },
        {
            "id": 1,
            "value_source": "method_result",
            "type": "amount",
            "decimals": 18,
            "to": uniswap_router_address,
            "method_name": "getAmountsOut",
            "method_params": [
                {
                    "input_id": 0
                },
                [token_address, weth_address]
            ],
            "method_result": 1
        },
        {
            "id": 2,
            "value_source": "deadline"
        }
    ]


def __get_buy_inputs(
        symbol: str,
        icon_url: str,
        decimals: int,
        token_address: str,
        swap_config: SwapConfig
):
    uniswap_router_address = swap_config.uniswap_v2_router_address
    weth_address = swap_config.weth_address

    return [
        {
            "id": 0,
            "value_source": "user_input",
            "description": f"Enter {symbol} amount",
            "type": "amount",
            "decimals": decimals,
            "symbol": symbol,
            "icon_url": icon_url
        },
        {
            "id": 1,
            "value_source": "deadline"
        },
        {
            "id": 2,
            "value_source": "method_result",
            "type": "amount",
            "to": uniswap_router_address,
            "method_name": "getAmountsIn",
            "method_params": [
                {
                    "input_id": 0
                },
                [weth_address, token_address]
            ],
            "method_result": 0
        }
    ]
