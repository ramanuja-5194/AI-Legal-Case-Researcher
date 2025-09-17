
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

class Settings(BaseSettings):
    google_api_key: str = Field(default="", alias="GOOGLE_API_KEY")
    llm_model: str = Field(default="gemini-1.5-pro", alias="LLM_MODEL")
    embedding_model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2", alias="EMBEDDING_MODEL")

    corpus_dir: str = Field(default="./src/legal_ai/data/corpus", alias="CORPUS_DIR")
    vectorstore_dir: str = Field(default="./src/legal_ai/data/vectorstore", alias="VECTORSTORE_DIR")

    indian_kanoon_api_key: str = Field(default="", alias="INDIAN_KANOON_API_KEY")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
Path(settings.corpus_dir).mkdir(parents=True, exist_ok=True)
Path(settings.vectorstore_dir).mkdir(parents=True, exist_ok=True)
