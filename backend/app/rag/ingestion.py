import os
import re
import logging
from typing import List, Dict, Any, Optional

# Set local NLTK data path if available
import nltk
from app.config import NLTK_LOCAL_DIR, settings

if NLTK_LOCAL_DIR.exists() and str(NLTK_LOCAL_DIR) not in nltk.data.path:
    nltk.data.path.insert(0, str(NLTK_LOCAL_DIR))

# Ensure robust offline verb classification in unstructured
try:
    import unstructured.partition.text_type as utt
    _common_verbs = {
        'is', 'are', 'was', 'were', 'have', 'has', 'had', 'do', 'does', 'did',
        'can', 'will', 'shall', 'may', 'must', 'be', 'been', 'being', 'eligible',
        'apply', 'submit', 'provide', 'study', 'receive', 'obtain', 'award', 'pursuing'
    }
    def _safe_contains_verb(text: str) -> bool:
        words = set(text.lower().split())
        return bool(words.intersection(_common_verbs))
    utt.contains_verb = _safe_contains_verb
except Exception:
    pass

from unstructured.partition.pdf import partition_pdf

logger = logging.getLogger("legalease.ingestion")

class PDFIngestionError(Exception):
    """Raised when PDF extraction or validation fails."""
    pass

class DocumentMetadata:
    def __init__(
        self,
        document_name: str,
        file_path: str,
        total_pages: int,
        scheme_name: str = "Unknown Scheme",
        source_url: str = "https://scholarships.gov.in",
        academic_year: str = "2024-25",
        last_verified_date: str = "2024-08-15"
    ):
        self.document_name = document_name
        self.file_path = file_path
        self.total_pages = total_pages
        self.scheme_name = scheme_name
        self.source_url = source_url
        self.academic_year = academic_year
        self.last_verified_date = last_verified_date

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_name": self.document_name,
            "file_path": self.file_path,
            "total_pages": self.total_pages,
            "scheme_name": self.scheme_name,
            "source_url": self.source_url,
            "academic_year": self.academic_year,
            "last_verified_date": self.last_verified_date,
        }

class PageExtract:
    def __init__(self, page_number: int, text: str, metadata: DocumentMetadata):
        self.page_number = page_number
        self.text = text
        self.metadata = metadata

    def to_dict(self) -> Dict[str, Any]:
        return {
            "page_number": self.page_number,
            "text": self.text,
            **self.metadata.to_dict()
        }

def sanitize_text(text: str) -> str:
    """Cleans extracted text by normalizing spaces and fixing broken linebreaks."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.replace("\xa0", " ")
    return text.strip()

def parse_scheme_metadata_from_text(first_page_text: str, filename: str) -> Dict[str, str]:
    """Extracts known scheme attributes and metadata from page text or filename."""
    metadata = {
        "scheme_name": os.path.splitext(filename)[0].replace("_", " "),
        "source_url": "https://scholarships.gov.in",
        "academic_year": "2024-25",
        "last_verified_date": "2024-08-15"
    }
    
    text_lower = first_page_text.lower()
    fn_lower = filename.lower()
    
    if "scholarships.punjab.gov.in" in text_lower or "punjab" in fn_lower:
        metadata["source_url"] = "https://scholarships.punjab.gov.in"
        metadata["scheme_name"] = "Post Matric Scholarship Scheme for SC Students (Punjab)"
    elif "yet.nta.ac.in" in text_lower or "yasasvi" in fn_lower:
        metadata["source_url"] = "https://yet.nta.ac.in"
        metadata["scheme_name"] = "PM-YASASVI Scholarship Scheme"
    elif "central sector" in text_lower or "csss" in fn_lower:
        metadata["source_url"] = "https://scholarships.gov.in"
        metadata["scheme_name"] = "PM-USP Central Sector Scheme of Scholarship"
    elif "means-cum-merit" in text_lower or "nmmss" in fn_lower:
        metadata["source_url"] = "https://scholarships.gov.in"
        metadata["scheme_name"] = "National Means-cum-Merit Scholarship Scheme (NMMSS)"

    date_match = re.search(r"Verified:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", first_page_text)
    if date_match:
        metadata["last_verified_date"] = date_match.group(1)
        
    year_match = re.search(r"Academic Year:\s*([0-9]{4}-[0-9]{2,4})", first_page_text)
    if year_match:
        metadata["academic_year"] = year_match.group(1)

    return metadata

def extract_pdf_document(file_path: str, custom_scheme_name: Optional[str] = None) -> List[PageExtract]:
    """
    Extracts text page-by-page from a PDF file using Unstructured (partition_pdf).
    Preserves page numbers, titles, and metadata for exact legal citations.
    """
    if not os.path.exists(file_path):
        raise PDFIngestionError(f"PDF file does not exist: {file_path}")

    filename = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    # 25 MB limit
    if file_size > 25 * 1024 * 1024:
        raise PDFIngestionError(f"File {filename} exceeds 25 MB size limit ({file_size} bytes).")

    try:
        elements = partition_pdf(filename=file_path, strategy="fast")
    except Exception as e:
        logger.warning(f"Unstructured partition_pdf failed on {filename}: {e}. Trying fallback...")
        import fitz
        try:
            doc = fitz.open(file_path)
            elements = []
            for p_idx, page in enumerate(doc):
                from unstructured.documents.elements import Text
                el = Text(page.get_text())
                el.metadata.page_number = p_idx + 1
                elements.append(el)
            doc.close()
        except Exception as fallback_e:
            raise PDFIngestionError(f"PDF extraction failed for {filename}: {str(e)} / {str(fallback_e)}")

    if not elements:
        raise PDFIngestionError(f"No readable text or elements extracted from {filename}")

    # Group extracted elements by page number
    pages_dict: Dict[int, List[str]] = {}
    for el in elements:
        p_num = getattr(el.metadata, "page_number", None) or 1
        txt = sanitize_text(el.text)
        if txt:
            if p_num not in pages_dict:
                pages_dict[p_num] = []
            pages_dict[p_num].append(txt)

    if not pages_dict:
        raise PDFIngestionError(f"Extracted content is empty for {filename}")

    total_pages = max(pages_dict.keys())
    first_page_text = "\n".join(pages_dict.get(1, []))
    parsed_meta = parse_scheme_metadata_from_text(first_page_text, filename)
    if custom_scheme_name:
        parsed_meta["scheme_name"] = custom_scheme_name

    doc_metadata = DocumentMetadata(
        document_name=filename,
        file_path=file_path,
        total_pages=total_pages,
        scheme_name=parsed_meta["scheme_name"],
        source_url=parsed_meta["source_url"],
        academic_year=parsed_meta["academic_year"],
        last_verified_date=parsed_meta["last_verified_date"]
    )

    page_extracts: List[PageExtract] = []
    for p_num in sorted(pages_dict.keys()):
        page_text = "\n\n".join(pages_dict[p_num])
        page_extract = PageExtract(
            page_number=p_num,
            text=page_text,
            metadata=doc_metadata
        )
        page_extracts.append(page_extract)

    logger.info(f"Ingested {filename} via Unstructured: {total_pages} pages, {len(elements)} elements.")
    return page_extracts
