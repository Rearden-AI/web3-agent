import logging

from langchain_core.runnables import Runnable

logger = logging.getLogger("answer_based_on_documentation")


class ChainLogger(Runnable):
    def invoke(self, obj, config=None):
        logger.info(obj)
        return obj
