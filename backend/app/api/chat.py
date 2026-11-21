from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.rag.pipeline import RAGPipeline

router = APIRouter(prefix="/api/chat", tags=["AI Assistant"])

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="User query")
    language: str = Field("en", description="Language preference: 'en', 'hi', or 'pa'")
    history: Optional[List[ChatMessage]] = Field(default=[], description="Prior conversation history")

class CitationItem(BaseModel):
    document_name: str
    page_number: int
    scheme_name: Optional[str] = None
    source_url: Optional[str] = None
    snippet: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    citations: List[CitationItem]
    confidence: str
    suggested_follow_ups: List[str]
    language: str
    retrieved_count: int
    timestamp: str

@router.post("", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    """
    RAG Chat endpoint:
    Performs scheme-contextualized FAISS similarity search,
    Cross-Encoder reranking, and generates grounded direct answers via Gemini
    with exact document and page citations in English, Hindi, or Punjabi.
    """
    query_text = payload.message.strip()
    if not query_text:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    rag = RAGPipeline.get_instance()
    
    # Convert history models to dicts
    history_dicts = [{"role": h.role, "content": h.content} for h in (payload.history or [])]

    # Execute RAG query with conversation context
    rag_result = rag.query(
        question=query_text,
        language=payload.language,
        history=history_dicts
    )

    return ChatResponse(
        answer=rag_result.get("answer", ""),
        citations=rag_result.get("citations", []),
        confidence=rag_result.get("confidence", "unverified"),
        suggested_follow_ups=rag_result.get("suggested_follow_ups", []),
        language=payload.language,
        retrieved_count=rag_result.get("retrieved_count", 0),
        timestamp=datetime.now(timezone.utc).isoformat()
    )
