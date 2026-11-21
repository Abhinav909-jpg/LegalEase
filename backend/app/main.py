import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.api.chat import router as chat_router
from app.api.schemes import router as schemes_router
from app.api.eligibility import router as eligibility_router
from app.api.documents import router as documents_router, sources_router
from app.rag.pipeline import RAGPipeline

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("legalease")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler: warms up RAG pipeline and indexes raw documents if needed."""
    logger.info("Initializing LegalEase backend services...")
    try:
        pipeline = RAGPipeline.get_instance()
        if not pipeline.retriever.chunks_corpus:
            logger.info("Corpus is empty. Starting initial ingestion of raw documents...")
            stats = pipeline.ingest_raw_directory()
            logger.info(f"Initial ingestion complete: {stats}")
        else:
            logger.info(f"Knowledge base ready with {len(pipeline.retriever.chunks_corpus)} chunks.")
    except Exception as e:
        logger.error(f"Error initializing RAG knowledge base: {e}", exc_info=True)
    yield
    logger.info("Shutting down LegalEase backend.")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="LegalEase - AI-Powered Government Scheme & Scholarship Navigator for Indian Citizens & Students",
    lifespan=lifespan
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred.", "error": str(exc)}
    )

@app.get("/api/health", tags=["Health"])
async def health_check():
    """System health check and diagnostic endpoint."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": settings.ENVIRONMENT,
        "rag_stack": {
            "pdf_extraction": "Unstructured (fast strategy)",
            "text_splitting": "CharacterTextSplitter",
            "embeddings": "Hugging Face Embeddings",
            "vector_storage": "FAISS",
            "retrieval": "Hugging Face Embeddings -> FAISS Similarity Search",
            "reranking": "Cross-Encoder (ms-marco-MiniLM-L-6-v2)",
            "generation": "Gemini (gemini-3.5-flash-lite)"
        },
        "capabilities": {
            "gemini_configured": bool(settings.GEMINI_API_KEY and settings.GEMINI_API_KEY.strip()),
            "embedding_model": settings.EMBEDDING_MODEL_NAME,
            "reranker_model": settings.CROSS_ENCODER_MODEL_NAME,
            "faiss_index_path": settings.FAISS_INDEX_PATH,
            "supported_languages": ["en", "hi", "pa"]
        }
    }

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to LegalEase API",
        "docs_url": "/docs",
        "health_check": "/api/health"
    }

# Include API Routers
app.include_router(chat_router)
app.include_router(schemes_router)
app.include_router(eligibility_router)
app.include_router(documents_router)
app.include_router(sources_router)
