import logging
import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import AsyncHtmlLoader, DirectoryLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ..classes.chat_message_flow_state import ChatMessageFlowState
from ...llm import get_model
from .....core.modules_factory import redis_db, tg_bot, kd

logger = logging.getLogger('answer_based_on_documentation')

model = get_model()

persist_directory = os.path.realpath(os.path.join(os.getcwd(), 'vstore'))

vector_store = Chroma(
    collection_name="knowledge",
    embedding_function=FastEmbedEmbeddings(cache_dir='/tmp/testdir'),
    persist_directory=persist_directory
)

# vector_store.delete_collection()

sources_in_store = list(set(map(lambda x: x['source'], vector_store.get()['metadatas'])))


def update_vectorstore(url_list: list):
    docs = AsyncHtmlLoader(web_path=url_list).load()
    knowledge_dir_path = os.path.realpath(os.path.join('app', "llm", "modules", "knowledge"))
    txt_docs = DirectoryLoader(path=knowledge_dir_path).load()

    html2text = Html2TextTransformer()
    docs = html2text.transform_documents(docs)

    docs += txt_docs
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
    chunks = text_splitter.transform_documents(docs)

    print('Start add to vectorstore')
    vector_store.add_documents(chunks)
    print('Finisdh add to vectorstore')

    vector_store.persist()


existing_urls = redis_db.lrange("knowledge_url", 0, -1)
decoded_urls = [url.decode('utf-8') for url in existing_urls]
if len(decoded_urls) < 1:
    decoded_urls.extend(
        ["https://docs.neonevm.org/docs/quick_start", "https://docs.starknet.io", "https://docs.wormhole.com/wormhole",
         "https://docs.sui.io"])
update_vectorstore(decoded_urls)

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

chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
)


def answer_based_on_documentation(state: ChatMessageFlowState):
    logger.info('Searching in documentation...')

    user_message = state['user_message']
    num_steps = int(state['num_steps'])
    num_steps += 1

    llm_response = chain.invoke(user_message)

    return {"num_steps": num_steps, "response": llm_response}


def update_knowledge():
    tg_bot.send_message(message="Knowledge update started!")
    urls, is_faq_updated = kd.update_all_data()
    if not is_faq_updated:
        tg_bot.send_message(message="Can't update FAQ. Auth token expired!")
    existing_urls = redis_db.lrange("knowledge_url", 0, -1)
    decoded_urls = [url.decode('utf-8') for url in existing_urls]
    new_urls = [url for url in urls if url not in decoded_urls]
    logging.info(f"NEW URLS: {new_urls}")
    if not new_urls:
        return
    url_str = "\n".join(new_urls)
    message = f"There are new urls added: {url_str}!"
    result = tg_bot.send_message(message=message)
    logging.info(f"Result of knowledge update send message: {result}")
    for value in new_urls:
        redis_db.rpush("knowledge_url", value)
    update_vectorstore(url_list=new_urls)
    tg_bot.send_message(message="Knowledge update finished!")
    return True
