import logging

from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from app.llm.modules.llm import get_model

from .logger import ChainLogger
from .prompt import prompt_template
from .vectorstore import get_retreiver

logger = logging.getLogger("answer_based_on_documentation")


chain_logger = ChainLogger()
model = get_model()

chain = (
    {"context": get_retreiver, "question": RunnablePassthrough(itemgetter("question"))}
    | prompt_template
    | chain_logger
    | model
    | StrOutputParser()
)


async def find_answer_in_documentation(question: str, tag: str = None):
    logger.info("Searching in documentation...")

    d = {"question": question}
    if tag:
        d["tag"] = tag

    llm_response = await chain.ainvoke(d)

    return llm_response
