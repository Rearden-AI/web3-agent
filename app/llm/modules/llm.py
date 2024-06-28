from app.core.config import ollama_config
from langchain_community.llms import Ollama

model = Ollama(model='llama3', base_url=ollama_config.OLLAMA_URL)


def initialize():
    pass


def get_model():
    return model
