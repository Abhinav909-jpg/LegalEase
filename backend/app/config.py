import os
import sys
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

# Set local NLTK data directory
NLTK_LOCAL_DIR = BASE_DIR / "nltk_data"
if NLTK_LOCAL_DIR.exists():
    import nltk
    if str(NLTK_LOCAL_DIR) not in nltk.data.path:
        nltk.data.path.insert(0, str(NLTK_LOCAL_DIR))

# Fast local model loading when requested offline
if os.environ.get("LEGAL_EASE_OFFLINE", "0") == "1":
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"

class Settings(BaseSettings):
    APP_NAME: str = "LegalEase API"
    APP_VERSION: str = "2.0.0"
    ENVIRONMENT: str = "development"
    
    # Gemini API
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.5-flash-lite"
    
    # Models
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    CROSS_ENCODER_MODEL_NAME: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    
    # FAISS Index
    FAISS_INDEX_PATH: str = str(BASE_DIR / "data" / "processed" / "faiss_index")
    
    # Chunking & Retrieval
    CHUNK_SIZE: int = 600
    CHUNK_OVERLAP: int = 100
    TOP_K_RETRIEVAL: int = 10
    TOP_K_RERANK: int = 5
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "*"
    ]
    
    # Paths
    RAW_DATA_DIR: str = str(BASE_DIR / "data" / "raw")
    PROCESSED_DATA_DIR: str = str(BASE_DIR / "data" / "processed")

    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()

# Ensure data directories exist
os.makedirs(settings.RAW_DATA_DIR, exist_ok=True)
os.makedirs(settings.PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(settings.FAISS_INDEX_PATH, exist_ok=True)
