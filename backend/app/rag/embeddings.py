import os
import logging
from typing import List
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import settings

logger = logging.getLogger("legalease.embeddings")

class MultilingualEmbeddingService:
    _instance = None

    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL_NAME
        logger.info(f"Loading Hugging Face Embeddings model: {self.model_name}")
        
        # Load HuggingFaceEmbeddings
        self.hf_embeddings = HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )
        # Test encode to determine dimension
        test_vec = self.hf_embeddings.embed_query("test")
        self.dimension = len(test_vec)
        logger.info(f"Hugging Face Embeddings ready. Dimension: {self.dimension}")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = MultilingualEmbeddingService()
        return cls._instance

    def embed_text(self, text: str) -> List[float]:
        """Embeds a single query or text."""
        if not text or not text.strip():
            return [0.0] * self.dimension
        return self.hf_embeddings.embed_query(text)

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embeds a batch of texts."""
        if not texts:
            return []
        return self.hf_embeddings.embed_documents(texts)

embedding_service = MultilingualEmbeddingService.get_instance
