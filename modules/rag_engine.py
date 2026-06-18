import os
import logging
import pdfplumber
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model cache for lazy loading
_model_cache = None

def get_embedding_model():
    """Get or initialize the embedding model (lazy loading)"""
    global _model_cache
    if _model_cache is None:
        logger.info("Loading SentenceTransformer model (this happens once)...")
        _model_cache = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("✅ Embedding model loaded successfully")
    return _model_cache


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file with error handling"""
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
        return text
    except Exception as e:
        logger.error(f"Error extracting text from {pdf_path}: {e}")
        return ""


def load_dataset_papers(dataset_folder: str = "dataset") -> List[Dict[str, str]]:
    """Load papers from dataset folder with error handling"""
    papers = []
    
    if not os.path.exists(dataset_folder):
        logger.warning(f"Dataset folder '{dataset_folder}' not found")
        return papers
    
    try:
        for file in os.listdir(dataset_folder):
            if file.endswith(".pdf"):
                path = os.path.join(dataset_folder, file)
                text = extract_text_from_pdf(path)
                if text:  # Only add if text extraction was successful
                    papers.append({
                        "filename": file,
                        "text": text[:3000]
                    })
        logger.info(f"✅ Loaded {len(papers)} papers from dataset")
    except Exception as e:
        logger.error(f"Error loading dataset papers: {e}")
    
    return papers


def create_embeddings(papers: List[Dict[str, str]]) -> Optional[np.ndarray]:
    """Create embeddings for papers with error handling"""
    if not papers:
        logger.warning("No papers provided for embedding")
        return None
    
    try:
        model = get_embedding_model()
        texts = [paper["text"] for paper in papers]
        embeddings = model.encode(texts)
        logger.info(f"✅ Created embeddings for {len(papers)} papers")
        return embeddings
    except Exception as e:
        logger.error(f"Error creating embeddings: {e}")
        return None


def create_faiss_index(embeddings: np.ndarray) -> Optional[faiss.IndexFlatL2]:
    """Create FAISS index from embeddings with error handling"""
    if embeddings is None:
        logger.error("No embeddings provided for FAISS index")
        return None
    
    try:
        embeddings = np.array(embeddings).astype("float32")
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        logger.info(f"✅ Created FAISS index with {embeddings.shape[0]} vectors")
        return index
    except Exception as e:
        logger.error(f"Error creating FAISS index: {e}")
        return None


def find_similar_papers(
    uploaded_text: str,
    papers: List[Dict[str, str]],
    index: faiss.IndexFlatL2,
    top_k: int = 3
) -> List[str]:
    """Find similar papers using FAISS index"""
    if not uploaded_text or not papers or index is None:
        logger.warning("Invalid inputs for similarity search")
        return []
    
    try:
        model = get_embedding_model()
        query_embedding = model.encode([uploaded_text[:3000]])
        query_embedding = np.array(query_embedding).astype("float32")
        
        distances, indices = index.search(query_embedding, min(top_k, len(papers)))
        
        results = []
        for idx in indices[0]:
            if 0 <= idx < len(papers):
                results.append(papers[idx]["filename"])
        
        logger.info(f"✅ Found {len(results)} similar papers")
        return results
    except Exception as e:
        logger.error(f"Error finding similar papers: {e}")
        return []
