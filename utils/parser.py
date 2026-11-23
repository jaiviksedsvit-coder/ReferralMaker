import io
import re
from typing import Optional
import pypdf

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts text content from PDF file bytes."""
    try:
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        extracted_text = []
        for page_idx, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                extracted_text.append(text)
        full_text = "\n".join(extracted_text).strip()
        # Clean extra whitespace
        full_text = re.sub(r'\n{3,}', '\n\n', full_text)
        return full_text
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

def extract_text_from_file(uploaded_file) -> Optional[str]:
    """Helper to extract text from various uploaded file formats (PDF, TXT)."""
    if uploaded_file is None:
        return None
    
    file_name = uploaded_file.name.lower()
    file_bytes = uploaded_file.getvalue()
    
    if file_name.endswith('.pdf'):
        return extract_text_from_pdf(file_bytes)
    elif file_name.endswith('.txt'):
        try:
            return file_bytes.decode('utf-8', errors='ignore')
        except Exception as e:
            return f"Error reading text file: {str(e)}"
    else:
        return None

def extract_key_bullets(resume_text: str, max_chars: int = 1500) -> str:
    """Condenses resume text into a concise summary to prevent token bloat."""
    if not resume_text:
        return ""
    lines = [l.strip() for l in resume_text.splitlines() if l.strip()]
    condensed = "\n".join(lines[:40])
    if len(condensed) > max_chars:
        return condensed[:max_chars] + "..."
    return condensed
