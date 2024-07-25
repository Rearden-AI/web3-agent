from pydantic_settings import BaseSettings


class ChromaSettings(BaseSettings):
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8000
