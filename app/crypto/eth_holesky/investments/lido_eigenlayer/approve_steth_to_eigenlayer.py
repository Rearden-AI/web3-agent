from app.crypto.eth_abstract.enums.contract_type import ContractType
from app.crypto.eth_abstract.services.abi_keeper import get_abi
from app.crypto.constants.links import ETH_ICON_URL
from .constants import STETH, EIGENLAYER_STRATEGY_MANAGER


approve_steth_to_eigenlayer = {
    "network": {
        "name": "Holesky",
        "icon": ETH_ICON_URL,
        "chain": {
            "type": "evm",
            "chainId": 17000
        }
    },
    "description": "Approve stETH on Eigenlayer",
    "type": "Approve",
    "transaction_data": {
        "to": STETH,
        "method_name": "approve",
        "method_params": [
            EIGENLAYER_STRATEGY_MANAGER,
            {"input_id": 0}
        ],
        "abis": {
            STETH: get_abi(ContractType.STETH)
        },
        "inputs": [
            {
                "id": 0,
                "value_source": "action_result",
                "description": "Enter stETH amount to approve",
                "action_id": 0,
                "return_id": 0
            },
        ],
        "returns": [
            {
                "id": 0,
                "value": {"input_id": 0}
            }
        ]
    },
    "balance_data": {
        "coin": STETH,
        "symbol": "stETH",
    }
}
