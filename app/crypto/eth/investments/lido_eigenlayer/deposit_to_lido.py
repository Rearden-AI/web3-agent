from app.crypto.eth_abstract.enums.contract_type import ContractType
from app.crypto.eth_abstract.services.abi_keeper import get_abi
from app.crypto.constants.links import ETH_ICON_URL, STETH_ICON_URL
from .constants import STETH


deposit_to_lido = {
    "network": {
        "name": "Mainnet",
        "icon": ETH_ICON_URL,
        "chain": {
            "type": "evm",
            "chainId": 1
        }
    },
    "description": "Deposit ETH to Lido",
    "type": "Deposit",
    "application_data": {
        "name": "Lido",
        "url": "https://lido.fi/",
        "contract_address": STETH,
        "contract_address_on_explorer": f"https://etherscan.io/address/{STETH}"
    },
    "parameters_description":
    [
        {
            "name": "From",
            "value": "ETH",
            "icon": ETH_ICON_URL
        },
        {
            "name": "To",
            "value": "stETH",
            "icon": STETH_ICON_URL
        },
        {
            "name": "APY",
            "value": "5-10%",
        }
    ],
    "transaction_data": {
        "to": STETH,
        "method_name": "submit",
        "method_params": [
            "0x0000000000000000000000000000000000000000"
        ],
        "value": {"input_id": 0},
        "abis": {
            STETH: get_abi(ContractType.STETH)
        },
        "inputs": [
            {
                "id": 0,
                "value_source": "user_input",
                "description": "Enter ETH amount to stake",
                "type": "amount",
                "decimals": 18
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
        "coin": "native",
        "symbol": "ETH",
    }
}
