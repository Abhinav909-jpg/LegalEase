import os
import re
import json
import logging
from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from rank_bm25 import BM25Okapi

from app.config import settings
from app.rag.chunking import DocumentChunk
from app.rag.embeddings import MultilingualEmbeddingService

logger = logging.getLogger("legalease.retrieval")

def tokenize_indic_and_english(text: str) -> List[str]:
    """Tokenizes text preserving English words and Indic script character tokens."""
    clean = re.sub(r"[^\w\s]", " ", text.lower())
    return clean.split()

def get_query_scheme_boost(query: str, doc_name: str, scheme_name: str) -> float:
    """Calculates priority multiplier when query explicitly names a specific scheme."""
    q = query.lower()
    target = (doc_name + " " + scheme_name).lower()
    
    if any(k in q for k in ["central sector", "csss", "pm-usp"]):
        if any(k in target for k in ["central_sector", "pm-usp", "central sector"]):
            return 3.0
    elif any(k in q for k in ["punjab", "post matric", "sc students", "freeship"]):
        if "punjab" in target:
            return 3.0
    elif any(k in q for k in ["yasasvi", "yet", "obc", "ebc"]):
        if "yasasvi" in target:
            return 3.0
    elif any(k in q for k in ["nmmss", "means-cum-merit", "means cum"]):
        if "nmmss" in target:
            return 3.0
            
    return 1.0

class FAISSRetriever:
    _instance = None

    def __init__(self):
        self.embedding_service = MultilingualEmbeddingService.get_instance()
        self.index_path = settings.FAISS_INDEX_PATH
        self.vectorstore: Optional[FAISS] = None
        self.chunks_corpus: List[Dict[str, Any]] = []
        self.bm25_index: Optional[BM25Okapi] = None
        
        self._load_or_init_faiss()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = FAISSRetriever()
        return cls._instance

    def _load_or_init_faiss(self):
        """Loads FAISS vectorstore and metadata from disk if available."""
        index_file = os.path.join(self.index_path, "index.faiss")
        meta_file = os.path.join(self.index_path, "chunks_corpus.json")
        
        if os.path.exists(index_file) and os.path.exists(meta_file):
            try:
                self.vectorstore = FAISS.load_local(
                    folder_path=self.index_path,
                    embeddings=self.embedding_service.hf_embeddings,
                    allow_dangerous_deserialization=True
                )
                with open(meta_file, "r", encoding="utf-8") as f:
                    self.chunks_corpus = json.load(f)
                
                if self.chunks_corpus:
                    tokenized = [tokenize_indic_and_english(c.get("text", "")) for c in self.chunks_corpus]
                    self.bm25_index = BM25Okapi(tokenized)
                logger.info(f"Loaded existing FAISS index with {len(self.chunks_corpus)} chunks.")
            except Exception as e:
                logger.warning(f"Could not load existing FAISS index: {e}. Reinitializing...")
                self.vectorstore = None
                self.chunks_corpus = []
                self.bm25_index = None

    def index_chunks(self, chunks: List[DocumentChunk]):
        """Indexes document chunks into FAISS vector storage with Hugging Face Embeddings."""
        if not chunks:
            return

        os.makedirs(self.index_path, exist_ok=True)
        docs = []
        for c in chunks:
            doc = Document(
                page_content=c.text,
                metadata=c.to_dict()
            )
            docs.append(doc)

        self.vectorstore = FAISS.from_documents(
            documents=docs,
            embedding=self.embedding_service.hf_embeddings
        )

        self.chunks_corpus = [c.to_dict() for c in chunks]

        # Save to disk
        self.vectorstore.save_local(self.index_path)
        meta_file = os.path.join(self.index_path, "chunks_corpus.json")
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(self.chunks_corpus, f, ensure_ascii=False, indent=2)

        # Refresh BM25
        tokenized = [tokenize_indic_and_english(c.get("text", "")) for c in self.chunks_corpus]
        self.bm25_index = BM25Okapi(tokenized) if tokenized else None

        logger.info(f"Successfully indexed {len(chunks)} chunks into FAISS vector store.")

    def search_faiss(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Retrieval: Hugging Face Embeddings -> FAISS Similarity Search."""
        if self.vectorstore is None:
            return []

        docs_and_scores = self.vectorstore.similarity_search_with_score(query, k=top_k)
        results = []
        for doc, score in docs_and_scores:
            meta = dict(doc.metadata)
            meta["text"] = doc.page_content
            meta["vector_score"] = float(score)
            results.append(meta)
        return results

    def search_bm25(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Performs lexical BM25 search over corpus."""
        if not self.bm25_index or not self.chunks_corpus:
            return []

        tokens = tokenize_indic_and_english(query)
        if not tokens:
            return []

        scores = self.bm25_index.get_scores(tokens)
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

        results = []
        for idx in top_indices:
            score = float(scores[idx])
            if score > 0:
                doc = dict(self.chunks_corpus[idx])
                doc["bm25_score"] = score
                results.append(doc)
        return results

    def hybrid_search(self, query: str, top_k: int = 12, rrf_k: int = 60) -> List[Dict[str, Any]]:
        """
        Retrieves candidates using FAISS Similarity Search combined with BM25 via Reciprocal Rank Fusion,
        with scheme-intent boosting.
        """
        faiss_results = self.search_faiss(query, top_k=max(top_k * 2, 16))
        bm25_results = self.search_bm25(query, top_k=max(top_k * 2, 16))

        rrf_scores: Dict[str, float] = {}
        chunks_map: Dict[str, Dict[str, Any]] = {}

        for rank, doc in enumerate(faiss_results):
            cid = doc.get("chunk_id", str(rank))
            chunks_map[cid] = doc
            boost = get_query_scheme_boost(query, doc.get("document_name", ""), doc.get("scheme_name", ""))
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (boost / (rrf_k + rank + 1))

        for rank, doc in enumerate(bm25_results):
            cid = doc.get("chunk_id", str(rank))
            if cid not in chunks_map:
                chunks_map[cid] = doc
            boost = get_query_scheme_boost(query, doc.get("document_name", ""), doc.get("scheme_name", ""))
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (boost / (rrf_k + rank + 1))

        sorted_cids = sorted(rrf_scores.keys(), key=lambda c: rrf_scores[c], reverse=True)
        return [chunks_map[cid] for cid in sorted_cids[:top_k]]
