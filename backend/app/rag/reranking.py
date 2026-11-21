import logging
from typing import List, Dict, Any
from sentence_transformers import CrossEncoder
from app.config import settings

logger = logging.getLogger("legalease.reranking")

class CrossEncoderReranker:
    _instance = None

    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.CROSS_ENCODER_MODEL_NAME
        logger.info(f"Loading Cross-Encoder Reranker model: {self.model_name}")
        try:
            # Prefer local cached files to prevent HF Hub network timeouts
            try:
                self.model = CrossEncoder(self.model_name, local_files_only=True)
            except Exception:
                self.model = CrossEncoder(self.model_name)
            logger.info("Cross-Encoder Reranker loaded successfully.")
        except Exception as e:
            logger.warning(f"Could not load CrossEncoder model ({e}). Fallback to RRF scores will be used.")
            self.model = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = CrossEncoderReranker()
        return cls._instance

    def rerank(self, query: str, candidate_chunks: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Reranks candidate chunks against the query using Cross-Encoder.
        Pairs: [[query, chunk.text], ...]
        """
        if not candidate_chunks:
            return []

        if not self.model or len(candidate_chunks) <= 1:
            return candidate_chunks[:top_k]

        try:
            pairs = [[query, chunk.get("text", "")] for chunk in candidate_chunks]
            scores = self.model.predict(pairs)

            for i, score in enumerate(scores):
                candidate_chunks[i]["rerank_score"] = float(score)

            reranked = sorted(candidate_chunks, key=lambda c: c.get("rerank_score", 0.0), reverse=True)
            return reranked[:top_k]
        except Exception as e:
            logger.error(f"Error during reranking: {e}. Falling back to input order.")
            return candidate_chunks[:top_k]

reranker_service = CrossEncoderReranker.get_instance
