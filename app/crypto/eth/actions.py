from .configs import swap_config
from ..eth_abstract.actions import SWAP, TRANSFER

available_actions = {
    SWAP: swap_config,
    TRANSFER: True
}
