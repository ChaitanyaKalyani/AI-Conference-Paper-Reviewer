import logging
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model cache for lazy loading
_model_cache = None

def get_embedding_model():
    """Get or initialize the embedding model (lazy loading)"""
    global _model_cache
    if _model_cache is None:
        logger.info("Loading SentenceTransformer model for ranker...")
        _model_cache = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("✅ Embedding model loaded")
    return _model_cache


def rank_papers(
    uploaded_text: str,
    papers: List[Dict[str, str]],
    top_k: int = 3
) -> List[Dict[str, str]]:
    """
    Rank papers by semantic similarity to uploaded text.
    
    Args:
        uploaded_text: The uploaded paper text
        papers: List of paper dictionaries with 'summary' key
        top_k: Number of top papers to return
    
    Returns:
        List of top-k similar papers ranked by similarity
    """
    if not uploaded_text or not papers:
        logger.warning("Invalid inputs for ranking papers")
        return []
    
    try:
        model = get_embedding_model()
        
        # Encode query
        query_embedding = model.encode([uploaded_text[:3000]])
        
        # Extract and encode paper summaries
        paper_texts = [
            paper.get("summary", "")
            for paper in papers
        ]
        
        # Filter out empty summaries
        valid_papers = [(paper, text) for paper, text in zip(papers, paper_texts) if text]
        
        if not valid_papers:
            logger.warning("No valid paper summaries found")
            return []
        
        valid_texts = [text for _, text in valid_papers]
        paper_embeddings = model.encode(valid_texts)
        
        # Calculate similarities
        similarities = cosine_similarity(query_embedding, paper_embeddings)[0]
        
        # Rank papers
        ranked = sorted(
            zip(similarities, [p for p, _ in valid_papers]),
            reverse=True
        )
        
        # Return top-k papers
        result = [paper for _, paper in ranked[:min(top_k, len(ranked))]]
        logger.info(f"✅ Ranked {len(result)} papers")
        return result
        
    except Exception as e:
        logger.error(f"Error ranking papers: {e}")
        return []
