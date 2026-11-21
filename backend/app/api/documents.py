import os
import shutil
import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from pydantic import BaseModel

from app.config import settings
from app.rag.pipeline import RAGPipeline
from app.rag.ingestion import PDFIngestionError

logger = logging.getLogger("schemesathi.documents")

router = APIRouter(prefix="/api/documents", tags=["Document Management"])
sources_router = APIRouter(prefix="/api/sources", tags=["Sources"])

class DocumentInfo(BaseModel):
    document_name: str
    file_size_bytes: int
    scheme_name: Optional[str] = None
    source_url: Optional[str] = None
    last_verified: Optional[str] = None

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    scheme_name: Optional[str] = Form(None)
):
    """
    Upload an official scheme/scholarship PDF to expand SchemeSathi's knowledge base.
    Validates PDF format and 25 MB file limit, then runs real ingestion, chunking,
    multilingual vector embedding, and Qdrant storage.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF documents are supported for ingestion."
        )

    # Sanitize filename
    safe_filename = "".join([c for c in file.filename if c.isalnum() or c in "._- "]).strip()
    if not safe_filename:
        safe_filename = "uploaded_guideline.pdf"

    target_path = os.path.join(settings.RAW_DATA_DIR, safe_filename)

    # Write file stream with size check (25 MB max)
    max_size = 25 * 1024 * 1024
    size = 0
    try:
        with open(target_path, "wb") as buffer:
            while chunk := await file.read(1024 * 64):
                size += len(chunk)
                if size > max_size:
                    buffer.close()
                    if os.path.exists(target_path):
                        os.remove(target_path)
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail="File exceeds maximum allowed size of 25 MB."
                    )
                buffer.write(chunk)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to save file: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not save file to disk."
        )

    # Trigger RAG pipeline ingestion
    try:
        rag = RAGPipeline.get_instance()
        ingest_summary = rag.ingest_single_file(target_path, scheme_name=scheme_name)
        return {
            "message": "Document uploaded and indexed successfully into RAG knowledge base.",
            "document_name": safe_filename,
            "pages_extracted": ingest_summary["pages"],
            "chunks_created": ingest_summary["chunks"],
            "status": "ready"
        }
    except PDFIngestionError as pe:
        if os.path.exists(target_path):
            os.remove(target_path)
        raise HTTPException(status_code=400, detail=str(pe))
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process and index PDF: {str(e)}")

@router.get("", response_model=List[DocumentInfo])
async def list_documents():
    """Lists all official government documents currently in the repository."""
    docs = []
    if os.path.exists(settings.RAW_DATA_DIR):
        for f in os.listdir(settings.RAW_DATA_DIR):
            if f.lower().endswith(".pdf"):
                fpath = os.path.join(settings.RAW_DATA_DIR, f)
                docs.append(DocumentInfo(
                    document_name=f,
                    file_size_bytes=os.path.getsize(fpath),
                    scheme_name=f.replace("_", " ").replace(".pdf", ""),
                    source_url="https://scholarships.gov.in",
                    last_verified="2024-08-15"
                ))
    return docs

@sources_router.get("/{source_id}")
async def get_source_details(source_id: str):
    """Retrieves metadata and page details for an official source document."""
    # Lookup in RAW_DATA_DIR
    target_file = None
    for f in os.listdir(settings.RAW_DATA_DIR):
        if source_id.lower() in f.lower():
            target_file = f
            break

    if not target_file:
        raise HTTPException(status_code=404, detail=f"Source document '{source_id}' not found.")

    filepath = os.path.join(settings.RAW_DATA_DIR, target_file)
    import fitz
    try:
        doc = fitz.open(filepath)
        total_pages = len(doc)
        doc.close()
    except Exception:
        total_pages = 1

    return {
        "source_id": source_id,
        "document_name": target_file,
        "total_pages": total_pages,
        "file_size_bytes": os.path.getsize(filepath),
        "source_url": "https://scholarships.gov.in",
        "last_verified_date": "2024-08-15"
    }
