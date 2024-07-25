import os
import logging

import chromadb

from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import AsyncHtmlLoader, DirectoryLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .modules_factory import redis_db, tg_bot, kd
from .config import chroma_settings

logger = logging.getLogger('vs_update')

client = chromadb.HttpClient(
    host=chroma_settings.CHROMA_HOST,
    port=chroma_settings.CHROMA_PORT
)

vector_store = Chroma(
    client=client,
    collection_name="knowledge",
    embedding_function=FastEmbedEmbeddings(cache_dir='/tmp/testdir')
)

sources_in_store = list(set(map(lambda x: x['source'], vector_store.get()['metadatas'])))


def update_vectorstore(url_list: list):
    logger.info(f"Updating vectorstore with {len(url_list)} links")

    docs = AsyncHtmlLoader(web_path=url_list).load()
    knowledge_dir_path = os.path.realpath(os.path.join("vectorstore_updater_app", "knowledge"))
    txt_docs = DirectoryLoader(path=knowledge_dir_path).load()

    html2text = Html2TextTransformer()
    docs = html2text.transform_documents(docs)

    docs += txt_docs
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
    chunks = text_splitter.transform_documents(docs)

    logger.info('Start add to vectorstore')
    vector_store.add_documents(chunks)
    logger.info('Finisdh add to vectorstore')


def update_knowledge():
    tg_bot.send_message(message="Knowledge update started!")
    logger.info('Start kd update all date')
    urls, is_faq_updated = kd.update_all_data()
    if not is_faq_updated:
        logger.info("Can't update FAQ.")
        tg_bot.send_message(message="Can't update FAQ. Auth token expired!")
    logger.debug('Finish kd update all data')
    existing_urls = redis_db.lrange("knowledge_url", 0, -1)
    decoded_urls = [url.decode('utf-8') for url in existing_urls]
    new_urls = [url for url in urls if url not in decoded_urls]
    logger.info(f"NEW URLS: {new_urls}")
    if new_urls or is_faq_updated:
        url_str = "\n".join(new_urls)
        message = f"There are new urls added: {url_str}!"
        result = tg_bot.send_message(message=message)
        logger.info(f"Result of knowledge update send message: {result}")
        for value in new_urls:
            redis_db.rpush("knowledge_url", value)
        try:
            update_vectorstore(url_list=new_urls)
        except Exception:
            logger.exception(f"ERROR vectorstore creating!")
            tg_bot.send_message(message="Update vectorstore unsuccessful!")
        finally:
            tg_bot.send_message(message="Knowledge update finished!")
    else:
        tg_bot.send_message(message="No urls to add")
    return True
