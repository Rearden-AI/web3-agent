from app.crypto.eth_abstract.enums.contract_type import ContractType
from app.crypto.eth_abstract.services.abi_keeper import get_abi
from app.crypto.constants.links import ETH_ICON_URL, STETH_ICON_URL
from .constants import STETH, STETH_EIGENLAYER_STRATEGY, EIGENLAYER_STRATEGY_MANAGER


restake_to_eigenlayer = {
    "network": {
        "name": "Mainnet",
        "icon": ETH_ICON_URL,
        "chain": {
            "type": "evm",
            "chainId": 1
        }
    },
    "description": "stETH restaking in Eigenlayer",
    "type": "Deposit",
    "application_data": {
        "name": "Eigenlayer",
        "url": "https://eigenlayer.xyz/",
        "contract_address": EIGENLAYER_STRATEGY_MANAGER,
        "contract_address_on_explorer": f"https://etherscan.io/address/{EIGENLAYER_STRATEGY_MANAGER}"
    },
    "parameters_description":
    [
        {
            "name": "In",
            "value": "stETH",
            "icon": STETH_ICON_URL
        },
        {
            "name": "APY",
            "value": "7-11%",
        }
    ],
    "transaction_data": {
        "to": EIGENLAYER_STRATEGY_MANAGER,
        "method_name": "depositIntoStrategy",
        "method_params": [
            STETH_EIGENLAYER_STRATEGY,
            STETH,
            {"input_id": 0}
        ],
        "abis": {
            EIGENLAYER_STRATEGY_MANAGER: get_abi(ContractType.EIGENLAYER_STRATEGY_MANAGER)
        },
        "inputs": [
            {
                "id": 0,
                "value_source": "action_result",
                "description": "Enter stETH amount to deposit",
                "action_id": 1,
                "return_id": 0
            },
        ]
    },
    "balance_data": {
        "coin": STETH,
        "symbol": "stETH",
    }
}
