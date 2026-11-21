import os
import glob
import logging
from typing import Dict, Any, List, Optional
from app.config import settings
from app.rag.ingestion import extract_pdf_document
from app.rag.chunking import chunk_extracted_pages, DocumentChunk
from app.rag.retrieval import FAISSRetriever
from app.rag.reranking import CrossEncoderReranker
from app.rag.generation import GroundedGenerator

logger = logging.getLogger("legalease.pipeline")

def resolve_contextual_query(question: str, history: Optional[List[Dict[str, str]]] = None) -> str:
    """
    Expands anaphoric queries (e.g. 'What are the required documents for this scheme?')
    with the active scheme identified from preceding conversation turns.
    """
    if not history:
        return question

    q_lower = question.lower()
    has_pronoun = any(p in q_lower for p in [
        "this scheme", "the scheme", "this scholarship", "for it", "for this", 
        "required documents", "how to apply", "documents needed", "eligibility criteria", "income limit"
    ])
    has_named_scheme = any(s in q_lower for s in [
        "central sector", "pm-usp", "csss", "punjab", "post matric", "sc students", "yasasvi", "nmmss", "means-cum-merit"
    ])

    if has_pronoun and not has_named_scheme:
        for msg in reversed(history):
            content = msg.get("content", "").lower()
            if any(k in content for k in ["central sector", "pm-usp", "csss"]):
                return f"{question} for PM-USP Central Sector Scheme of Scholarship (CSSS)"
            if any(k in content for k in ["punjab", "post matric"]):
                return f"{question} for Post Matric Scholarship Scheme for SC Students in Punjab"
            if "yasasvi" in content:
                return f"{question} for PM-YASASVI Scholarship Scheme"
            if any(k in content for k in ["means-cum-merit", "nmmss"]):
                return f"{question} for National Means-cum-Merit Scholarship Scheme (NMMSS)"

    return question

class RAGPipeline:
    _instance = None

    def __init__(self):
        self.retriever = FAISSRetriever.get_instance()
        self.reranker = CrossEncoderReranker.get_instance()
        self.generator = GroundedGenerator.get_instance()
        
        # Populate FAISS knowledge base if empty
        if not self.retriever.chunks_corpus:
            logger.info("Initializing FAISS knowledge base from raw documents...")
            self.ingest_raw_directory()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = RAGPipeline()
        return cls._instance

    def ingest_single_file(self, file_path: str, scheme_name: str = None) -> Dict[str, Any]:
        """Ingests, chunks, and indexes a single PDF document using Unstructured, CharacterTextSplitter, and FAISS."""
        pages = extract_pdf_document(file_path, custom_scheme_name=scheme_name)
        chunks = chunk_extracted_pages(
            pages,
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        self.retriever.index_chunks(chunks)
        return {
            "file": os.path.basename(file_path),
            "pages": len(pages),
            "chunks": len(chunks)
        }

    def ingest_raw_directory(self) -> Dict[str, Any]:
        """Scans the raw data directory and indexes all PDF documents."""
        pdf_pattern = os.path.join(settings.RAW_DATA_DIR, "*.pdf")
        pdf_files = glob.glob(pdf_pattern)
        logger.info(f"Found {len(pdf_files)} PDF files in {settings.RAW_DATA_DIR}")

        total_pages = 0
        total_chunks = 0
        all_chunks: List[DocumentChunk] = []

        for pdf_path in pdf_files:
            try:
                pages = extract_pdf_document(pdf_path)
                chunks = chunk_extracted_pages(
                    pages,
                    chunk_size=settings.CHUNK_SIZE,
                    chunk_overlap=settings.CHUNK_OVERLAP
                )
                all_chunks.extend(chunks)
                total_pages += len(pages)
                total_chunks += len(chunks)
            except Exception as e:
                logger.error(f"Error ingesting {pdf_path}: {e}")

        if all_chunks:
            self.retriever.index_chunks(all_chunks)

        return {
            "documents_indexed": len(pdf_files),
            "total_pages": total_pages,
            "total_chunks": total_chunks
        }

    def query(
        self,
        question: str,
        language: str = "en",
        top_k_retrieve: int = None,
        top_k_rerank: int = None,
        history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Executes end-to-end RAG pipeline:
        1. Contextual Query Resolution (handles 'this scheme', 'it', etc. from conversation history)
        2. FAISS Similarity Search + BM25 Hybrid Retrieval with scheme intent boosting
        3. Cross-Encoder Reranking
        4. Grounded Direct Answer Generation via Gemini with page citations
        """
        if not self.retriever.chunks_corpus:
            self.ingest_raw_directory()

        resolved_query = resolve_contextual_query(question, history)
        logger.info(f"Resolved query: '{resolved_query}' (original: '{question}')")

        retrieve_k = top_k_retrieve or max(settings.TOP_K_RETRIEVAL, 16)
        rerank_k = top_k_rerank or max(settings.TOP_K_RERANK, 6)

        # 1. FAISS + BM25 Hybrid Search
        candidate_chunks = self.retriever.hybrid_search(resolved_query, top_k=retrieve_k)
        if not candidate_chunks:
            candidate_chunks = self.retriever.search_faiss(resolved_query, top_k=retrieve_k)

        # 2. Cross-Encoder Reranking
        reranked_chunks = self.reranker.rerank(resolved_query, candidate_chunks, top_k=rerank_k)

        # 3. Grounded Answer Generation with Gemini
        result = self.generator.generate_grounded_answer(
            query=resolved_query,
            passages=reranked_chunks,
            language=language,
            history=history
        )

        result["resolved_query"] = resolved_query
        result["retrieved_count"] = len(candidate_chunks)
        result["reranked_count"] = len(reranked_chunks)
        result["top_chunks"] = [
            {
                "chunk_id": c.get("chunk_id"),
                "document_name": c.get("document_name"),
                "page_number": c.get("page_number"),
                "scheme_name": c.get("scheme_name"),
                "source_url": c.get("source_url"),
                "rerank_score": c.get("rerank_score"),
                "text": c.get("text")
            }
            for c in reranked_chunks
        ]
        return result

rag_pipeline = RAGPipeline.get_instance
