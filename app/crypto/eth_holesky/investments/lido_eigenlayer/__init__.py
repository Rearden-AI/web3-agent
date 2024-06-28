from app.crypto.eth.classes.investment_strategy import InvestmentStrategy
from .deposit_to_lido import deposit_to_lido
from .approve_steth_to_eigenlayer import approve_steth_to_eigenlayer
from .restake_to_eigenlayer import restake_to_eigenlayer

KEY="lido_eigen"

strategy = InvestmentStrategy(
    name="Deposit to Lido + Restake to Eigenlayer",
    key=KEY,
    approxApy=40
)
actions = [
    {
        "id": 0,
        "action_data": deposit_to_lido
    },
    {
        "id": 1,
        "action_data": approve_steth_to_eigenlayer
    },
    {
        "id": 2,
        "action_data": restake_to_eigenlayer
    }
]
