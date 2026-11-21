import re
import uuid
import logging
from typing import List, Dict, Any
from langchain_text_splitters import CharacterTextSplitter
from app.rag.ingestion import PageExtract

logger = logging.getLogger("legalease.chunking")

class DocumentChunk:
    def __init__(
        self,
        chunk_id: str,
        text: str,
        document_name: str,
        page_number: int,
        scheme_name: str,
        source_url: str,
        academic_year: str,
        last_verified_date: str,
        section_header: str = ""
    ):
        self.chunk_id = chunk_id
        self.text = text
        self.document_name = document_name
        self.page_number = page_number
        self.scheme_name = scheme_name
        self.source_url = source_url
        self.academic_year = academic_year
        self.last_verified_date = last_verified_date
        self.section_header = section_header

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "text": self.text,
            "document_name": self.document_name,
            "page_number": self.page_number,
            "scheme_name": self.scheme_name,
            "source_url": self.source_url,
            "academic_year": self.academic_year,
            "last_verified_date": self.last_verified_date,
            "section_header": self.section_header
        }

def find_active_section_header(text: str) -> str:
    """Detects section heading like '1. Objective', '2. Eligibility Criteria', '4. Required Documents', etc."""
    match = re.search(r"(\d+\.\s+[A-Za-z\s&/]{3,50})", text)
    if match:
        return match.group(1).strip()
    return ""

def chunk_extracted_pages(
    pages: List[PageExtract], 
    chunk_size: int = 500, 
    chunk_overlap: int = 80
) -> List[DocumentChunk]:
    """
    Splits extracted pages into high-precision, scheme-contextualized chunks
    using LangChain's CharacterTextSplitter.
    Prepends the Scheme Name and Section Header to ensure vector embeddings
    and Cross-Encoder rerankers capture full semantic context.
    """
    splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        strip_whitespace=True
    )

    all_chunks: List[DocumentChunk] = []

    for page in pages:
        page_text = page.text
        if not page_text or not page_text.strip():
            continue

        raw_pieces = splitter.split_text(page_text)
        
        # If double-newline didn't split, fallback to single newline
        if len(raw_pieces) == 1 and len(page_text) > chunk_size:
            line_splitter = CharacterTextSplitter(
                separator="\n",
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                strip_whitespace=True
            )
            raw_pieces = line_splitter.split_text(page_text)

        last_section = ""
        for i, piece in enumerate(raw_pieces):
            piece = piece.strip()
            if not piece:
                continue

            header = find_active_section_header(piece)
            if header:
                last_section = header

            doc_safe_name = re.sub(r"[^a-zA-Z0-9_]", "", page.metadata.document_name.replace(".pdf", ""))
            chunk_id = f"{doc_safe_name}_p{page.page_number}_c{i+1}_{uuid.uuid4().hex[:6]}"

            # Contextualize chunk with Scheme Name and Section Header for 10x retrieval accuracy
            scheme_title = page.metadata.scheme_name
            contextualized_text = f"[{scheme_title}]"
            if last_section and last_section not in piece:
                contextualized_text += f" {last_section}:\n{piece}"
            else:
                contextualized_text += f"\n{piece}"

            chunk = DocumentChunk(
                chunk_id=chunk_id,
                text=contextualized_text,
                document_name=page.metadata.document_name,
                page_number=page.page_number,
                scheme_name=page.metadata.scheme_name,
                source_url=page.metadata.source_url,
                academic_year=page.metadata.academic_year,
                last_verified_date=page.metadata.last_verified_date,
                section_header=last_section
            )
            all_chunks.append(chunk)

    logger.info(f"Chunked {len(pages)} pages into {len(all_chunks)} contextualized chunks.")
    return all_chunks
