from typing import Any

from app.crypto.eth.classes.investment_strategy import InvestmentStrategy

from . import lido_eigenlayer


investment_strategies: list[InvestmentStrategy] = []
investment_actions: dict[str, Any] = {}

investment_strategies.append(lido_eigenlayer.strategy)
investment_actions[lido_eigenlayer.KEY] = lido_eigenlayer.actions


def get_investment_stratrgies():
    return investment_strategies
