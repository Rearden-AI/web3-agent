import logging

from app.crypto.eth.investments import get_investment_stratrgies

from ...classes import ChatMessageFlowState

logger = logging.getLogger('invest_action')

def invest_action(state: ChatMessageFlowState):
    logger.info('Processing investment action')
    
    user_message = state['user_message']
    num_steps = int(state['num_steps'])
    num_steps += 1

    return {
        "num_steps": num_steps,
        "response": "Looks like you want to invest some funds. We can offer you several strategies:",
        "chooseable_actions": get_investment_stratrgies()
    }