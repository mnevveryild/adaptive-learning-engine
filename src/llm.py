from functools import lru_cache
from langchain_openai import OpenAIEmbeddings
from src.config import EMBED_MODEL

@lru_cache(maxsize=None)

def get_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model=EMBED_MODEL)