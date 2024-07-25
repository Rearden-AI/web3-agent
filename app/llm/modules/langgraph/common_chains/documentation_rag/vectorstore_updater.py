import logging

from operator import itemgetter

from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.modules_factory import tg_bot, kd

from .vectorstore import vector_store

logger = logging.getLogger("answer_based_on_documentation/vectorstore_updater")

projects = [
    {
        "tag": "wormhole",
        "links": [
            "https://docs.wormhole.com/wormhole",
            {
                "url": "https://portalbridge.com/docs",
                "starts_with": "https://portalbridge.com/docs/",
            },
        ],
    },
    {"tag": "starknet", "links": ["https://docs.starknet.io"]},
    {"tag": "neon", "links": ["https://docs.neonevm.org/docs/quick_start"]},
    {"tag": "sui", "links": ["https://docs.sui.io"]},
]


def update_vectorstore(url_list: list, tag: str):
    logger.info("Updating vectorstore with %d links", len(url_list))

    docs = AsyncHtmlLoader(web_path=url_list).load()

    html2text = Html2TextTransformer()
    docs = html2text.transform_documents(docs)

    for doc in docs:
        doc.metadata["tag"] = tag

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
    chunks = text_splitter.transform_documents(docs)

    if len(chunks) == 0:
        return

    logger.info("Start adding %d chunks to vectorstore", len(chunks))
    vector_store.add_documents(chunks)
    logger.info("Finisdh add to vectorstore")


def update_knowledge():
    tg_bot.send_message(message="Knowledge update started!")
    logger.info("Start kd update all data")

    try:
        __update_knowledge_logic()
    except Exception:
        logger.exception("ERROR vectorstore creating!")
        tg_bot.send_message(message="Update vectorstore unsuccessful!")
    finally:
        tg_bot.send_message(message="Knowledge update finished!")


def __update_knowledge_logic():
    urls_in_vectorstore = list(
        map(itemgetter("source"), vector_store.get()["metadatas"])
    )

    for project in projects:
        tag = project["tag"]
        logger.debug("Start %s update", tag)

        project_links = []
        for link in project["links"]:
            project_links += kd.parse_all_links(link)

        new_urls = [url for url in project_links if url not in urls_in_vectorstore]
        logger.info(
            "got %d links for %s, %d new", len(project_links), tag, len(new_urls)
        )

        if len(new_urls) > 0:
            url_str = "\n".join(new_urls)
            message = f"There are new urls added to {tag}: {url_str}"
            tg_bot.send_message(message=message)

            update_vectorstore(url_list=new_urls, tag=tag)

        logger.debug("Finished %s update", tag)


# logger.info("Updating knowledgebase")
# update_knowledge()
# logger.info("Finished updating")
