import logging

from consts import (
    tokens,
    contracts
)


def transfer_erc20_token():
    _unsigned_transactions = []
    target_abi_part = {
        'constant': False,
        'inputs': [
            {
                'name': '_to',
                'type': 'address'
            },
            {
                'name': '_value',
                'type': 'uint256'
            }
        ],
        'name': 'transfer',
        'outputs': [
            {
                'name': '',
                'type': 'bool'
            }
        ],
        'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    }

    tokens_list = {
        "DAI": tokens.DAI,
        "USDC": tokens.USDC,
        "USDT": tokens.USDT,
        "wETH": tokens.wETH,
        "wBTC": tokens.wBTC,
        "stETH": tokens.stETH,
    }

    _action = {
        "action_type": "transaction",
        "details": {
            "name": "Transfer ERC-20 token",
            "dapp_link": "",
            "apy": ""
        },
        "body": {
            # "token_address": tokens.stETH,
            # "contract_address": contracts,
            "abi": target_abi_part,
            "arguments": [{"name": "_to", "value": ""}, {"name": "_value"}],
        },
        "tokens_list": tokens_list
    }
    _unsigned_transactions.append(_action)
    return _unsigned_transactions


def deposit_steth_eigenlayer():
    _unsigned_transactions = []
    target_abi_part = {
        'constant': False,
        'inputs': [
            {
                'name': '_spender',
                'type': 'address'
            },
            {
                'name': '_amount',
                'type': 'uint256'
            }
        ],
        'name': 'approve',
        'outputs': [
            {
                'name': '',
                'type': 'bool'
            }
        ],
        'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    }

    _action = {
        "action_type": "transaction",
        "details": {
            "name": "Approve stETH on Eigenlayer",
            "dapp_link": "https://eigenlayer.xyz/",
            "apy": "7-11%"
        },
        "body": {
            "token_address_in": tokens.stETH,
            "token_address_out": tokens.stETH,
            "contract_address": contracts.eigenlayer,
            "abi": target_abi_part,
            "arguments": [
                {"name": "_spender", "value": contracts.eigenlayer_spender},
                {"name": "_amount"}
            ],
        },
    }
    _unsigned_transactions.append(_action)
    target_abi_part = {
        'inputs': [
            {
                'internalType': 'contractIStrategy',
                'name': 'strategy',
                'type': 'address'
            },
            {
                'internalType': 'contractIERC20',
                'name': 'token',
                'type': 'address'
            },
            {
                'internalType': 'uint256',
                'name': 'amount',
                'type': 'uint256'
            }
        ],
        'name': 'depositIntoStrategy',
        'outputs': [
            {
                'internalType': 'uint256',
                'name': 'shares',
                'type': 'uint256'
            }
        ],
        'stateMutability': 'nonpayable',
        'type': 'function'
    }

    _action = {
        "action_type": "transaction",
        "details": {
            "name": "Deposit into strategy",
            "dapp_link": "https://eigenlayer.xyz/",
            "apy": "7-11%"
        },
        "body": {
            "token_address_in": tokens.stETH,
            "token_address_out": tokens.stETH,
            "contract_address": contracts.eigenlayer_manager,
            "abi": target_abi_part,
            "arguments": [
                {"name": "strategy", "value": contracts.eigenlayer_strategy},
                {"name": "token", "value": tokens.stETH},
                {"name": "amount"},
            ],
        },
    }
    _unsigned_transactions.append(_action)

    return _unsigned_transactions


def deposit_eth_lido() -> list:
    _unsigned_transactions = []
    target_abi_part = {
        'constant': False,
        'inputs': [
            {
                'name': '_referral',
                'type': 'address'
            }
        ],
        'name': 'submit',
        'outputs': [
            {
                'name': '',
                'type': 'uint256'
            }
        ],
        'payable': True,
        'stateMutability': 'payable',
        'type': 'function'
    }
    _action = {
        "action_type": "transaction",
        "details": {
            "name": "Deposit ETH to Lido",
            "dapp_link": "https://lido.fi/",
            "apy": "5-10%"
        },
        "body": {
            # "token_address": tokens.stETH,

            "token_address_in": None,
            "token_address_out": tokens.stETH,
            "contract_address": contracts.lido,
            "abi": target_abi_part,
            "arguments": [{"name": "_referral", "value": contracts.lido_referral}],
        },
    }
    _unsigned_transactions.append(_action)
    return _unsigned_transactions


def send_transaction():
    return []


async def build_strategy(steps: list) -> list:
    scope = {
        "deposit_steth_eigenlayer": deposit_steth_eigenlayer,
        "transfer_erc20_token": transfer_erc20_token,
        "deposit_eth_lido": deposit_eth_lido,
        "send_transaction": send_transaction
    }
    strategy = []
    for step in steps:
        try:
            strategy += scope[step]()
        except KeyError:
            logging.debug(f"Step {step} not found in scope")

    return strategy
