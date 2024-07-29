import chromadb

from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma

from .config import ChromaSettings


chroma_settings = ChromaSettings()

client = chromadb.HttpClient(
    host=chroma_settings.CHROMA_HOST, port=chroma_settings.CHROMA_PORT
)

vector_store = Chroma(
    client=client,
    collection_name="knowledge",
    embedding_function=FastEmbedEmbeddings(cache_dir="/tmp/testdir"),
)


def get_retreiver(input):
    if "tag" in input:
        search_kwargs = {"filter": {"tag": input["tag"]}}
    else:
        search_kwargs = {}

    return vector_store.as_retriever(search_kwargs=search_kwargs)