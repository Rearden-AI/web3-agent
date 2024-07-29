import os
import logging
from operator import itemgetter

from langchain_community.document_loaders import AsyncHtmlLoader, DirectoryLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .modules_factory import redis_db, tg_bot, kd
from .vectorstore import vector_store

logger = logging.getLogger('vs_update')

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
        "blog_link": "https://wormhole.com/blog",
        "discord_faq_link": "https://discord.com/api/v9/channels/1075310129798459492/threads/search?archived=true&sort_by=last_message_time&sort_order=desc&limit=25&tag_setting=match_some&offset=0"
    },
    {"tag": "starknet", "links": ["https://docs.starknet.io"]},
    {
        "tag": "neon",
        "links": ["https://docs.neonevm.org/docs/quick_start"],
        "blog_link": "https://neonevm.org/blog",
        "discord_faq_link": "https://discord.com/api/v9/channels/1176488632933163078/messages?limit=50"},

    {"tag": "sui", "links": ["https://docs.sui.io"]},
]


def update_vectorstore_urls(url_list: list, tag: str, is_faq_updated: bool = False):
    logger.info("Updating vectorstore with %d links", len(url_list))

    docs = AsyncHtmlLoader(web_path=url_list).load()

    html2text = Html2TextTransformer()
    docs = html2text.transform_documents(docs)

    if is_faq_updated:
        knowledge_dir_path = os.path.realpath(
            os.path.join("vectorstore_updater_app", "knowledge", f"{tag}_discord.txt"))
        txt_docs = DirectoryLoader(path=knowledge_dir_path).load()
        docs += txt_docs

    for doc in docs:
        doc.metadata["tag"] = tag

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
    chunks = text_splitter.transform_documents(docs)

    if len(chunks) == 0:
        return

    logger.info("Start adding %d chunks to vectorstore", len(chunks))
    vector_store.add_documents(chunks)
    logger.info('Finisdh add to vectorstore')


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
            project_links += kd.parse_all_links(initial_page=link)

        blog_link = project.get("blog_link")
        if blog_link:
            project_links += kd.update_blog_posts(link=blog_link)

        new_urls = [url for url in project_links if url not in urls_in_vectorstore]
        logger.info(
            "got %d links for %s, %d new", len(project_links), tag, len(new_urls)
        )

        faq_link = project.get("discord_faq_link")
        faq_result = False
        if faq_link:
            faq_result = kd.update_discord_faq(link=faq_link, protocol_name=tag)
            logging.critical("Can't update FAQ!")

        if len(new_urls) > 0:
            url_str = "\n".join(new_urls)
            message = f"There are new urls added to {tag}: {url_str}"
            tg_bot.send_message(message=message)

            update_vectorstore_urls(url_list=new_urls, tag=tag, is_faq_updated=faq_result)
        else:
            logging.info("No urls to add")

        logger.debug("Finished %s update", tag)
