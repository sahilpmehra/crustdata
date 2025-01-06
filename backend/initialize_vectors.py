import asyncio
import pdfplumber
from dataclasses import dataclass
from config_prod import OPENAI_API_KEY, PDF_PATHS
from services.vector_store import VectorStoreService

@dataclass
class DocSection:
    content: str
    url: str  # will be the PDF path in this case
    title: str
    section: str

def clean_text(text):
    import re
    # Replace multiple newlines or spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text, pdf_path, chunk_size=250, overlap=25):
    words = text.split()
    chunks = []
    metadatas = []
    start = 0
    chunk_number = 1
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])  # Join words into a string
        # Create DocSection object for each chunk
        doc_section = DocSection(
            content=chunk,
            url=pdf_path,
            title=pdf_path.split('/')[-1],
            section=f"Chunk {chunk_number}"
        )
        metadatas.append(doc_section.__dict__)  # Convert dataclass to dict
        chunks.append(chunk)  # Now appending string instead of list of words
        start += chunk_size - overlap
        chunk_number += 1
    return chunks, metadatas

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text.strip()

async def initialize_vector_store():
    vector_store = VectorStoreService(OPENAI_API_KEY)
    
    all_sections = []
    all_metadatas = []
    for pdf_path in PDF_PATHS:
        # Extract text from PDF
        raw_text = extract_text_from_pdf(pdf_path)
        # Clean the text
        cleaned_text = clean_text(raw_text)
        # Create chunks as DocSection objects
        chunks, metadatas = chunk_text(cleaned_text, pdf_path)
        all_sections.extend(chunks)
        all_metadatas.extend(metadatas)
    
    vector_store.create_embeddings(all_sections, all_metadatas)
    return vector_store

if __name__ == "__main__":
    asyncio.run(initialize_vector_store())
