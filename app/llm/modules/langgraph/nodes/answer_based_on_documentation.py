import logging

import chromadb

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, Runnable
from langchain_core.prompts import PromptTemplate
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.modules_factory import redis_db, tg_bot, kd
from app.core.config import chroma_settings
from ..classes.chat_message_flow_state import ChatMessageFlowState
from ...llm import get_model

logger = logging.getLogger('answer_based_on_documentation')

model = get_model()

client = chromadb.HttpClient(
    host=chroma_settings.CHROMA_HOST,
    port=chroma_settings.CHROMA_PORT
)

vector_store = Chroma(
    client=client,
    collection_name="knowledge",
    embedding_function=FastEmbedEmbeddings(cache_dir='/tmp/testdir')
)

# vector_store.delete_collection()

sources_in_store = list(set(map(lambda x: x['source'], vector_store.get()['metadatas'])))


def update_vectorstore(url_list: list):
    logger.info(f"Updating vectorstore with {len(url_list)} links")

    docs = AsyncHtmlLoader(web_path=url_list).load()

    html2text = Html2TextTransformer()
    docs = html2text.transform_documents(docs)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
    chunks = text_splitter.transform_documents(docs)

    logger.info('Start add to vectorstore')
    vector_store.add_documents(chunks)
    logger.info('Finisdh add to vectorstore')


# existing_urls = redis_db.lrange("knowledge_url", 0, -1)
# decoded_urls = [url.decode('utf-8') for url in existing_urls]
# if len(decoded_urls) < 1:
#     decoded_urls.extend(
#         [
#             "https://docs.neonevm.org/docs/quick_start",
#             "https://docs.starknet.io",
#             "https://docs.wormhole.com/wormhole",
#             "https://docs.sui.io"
#         ])
# update_vectorstore(decoded_urls)

retriever = vector_store.as_retriever()

prompt = PromptTemplate.from_template(
    """
    You are an expert in blockchain products consulting.\
    You help newcomers to go deep in crypto world.\
    You know everything about crypto projects.\
    Reply in short, simple and friendly manner.\
    Use provided context to answer user's question.\
    If you can't answer the question, tell so.\
    User doesn't know anything about context, context is your knowledge, don't mention word \"context\" in the answer, use \"knowledgebase\" instead.
        
    Context: {context}

    Question: {question}
    """
)

class ChainLogger(Runnable):
    def invoke(self, obj, config = None):
        logger.info(obj)
        return obj

chain_logger = ChainLogger()

chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | chain_logger
        | model
        | StrOutputParser()
)


async def answer_based_on_documentation(state: ChatMessageFlowState):
    logger.info('Searching in documentation...')

    user_message = state['user_message']
    num_steps = int(state['num_steps'])
    num_steps += 1

    llm_response = await chain.ainvoke(user_message)

    return {"num_steps": num_steps, "response": llm_response}


def update_knowledge():
    tg_bot.send_message(message="Knowledge update started!")
    logger.info('Start kd update all date')
    urls = kd.update_all_data()
    logger.debug('Finish kd update all data')
    existing_urls = redis_db.lrange("knowledge_url", 0, -1)
    decoded_urls = [url.decode('utf-8') for url in existing_urls]
    new_urls = [url for url in urls if url not in decoded_urls]
    logger.info(f"NEW URLS: {new_urls}")
    if not new_urls:
        return
    url_str = "\n".join(new_urls)
    message = f"There are new urls added: {url_str}!"
    result = tg_bot.send_message(message=message)
    logger.info(f"Result of knowledge update send message: {result}")
    for value in new_urls:
        redis_db.rpush("knowledge_url", value)
    try:
        update_vectorstore(url_list=new_urls)
    except Exception:
        logging.exception(f"ERROR vectorstore creating!")
        tg_bot.send_message(message="Update vectorstore unsuccessful!")
    finally: tg_bot.send_message(message="Knowledge update finished!")
    tg_bot.send_message(message="Knowledge update finished!")
    return True


# logger.info('Updating knowledgebase')
# update_knowledge()
# logger.info('Finished updating')
