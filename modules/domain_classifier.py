import logging
import re
from typing import Tuple, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define domain keywords with weights
DOMAIN_KEYWORDS = {
    "Natural Language Processing": [
        ("nlp", 2), ("bert", 2), ("transformer", 2), ("language model", 2),
        ("tokenization", 1.5), ("sentiment analysis", 2), ("named entity", 2),
        ("text classification", 2), ("seq2seq", 1.5), ("attention mechanism", 1.5),
        ("word embedding", 1.5), ("question answering", 1.5), ("machine translation", 2)
    ],
    
    "Computer Vision": [
        ("image", 1), ("object detection", 2), ("yolo", 2), ("cnn", 1.5),
        ("opencv", 1.5), ("segmentation", 2), ("vision", 1), ("image processing", 1.5),
        ("convolutional", 1.5), ("faster rcnn", 2), ("face recognition", 2),
        ("visual", 1), ("pixel", 1), ("filter", 0.5)
    ],
    
    "Machine Learning": [
        ("machine learning", 2), ("meta-learning", 2), ("reasoning", 1),
        ("agent", 1), ("agentic", 1.5), ("optimization", 1), ("reinforcement learning", 2),
        ("pareto", 1.5), ("design synthesis", 1.5), ("llm", 1), ("algorithm", 0.5),
        ("model", 0.5), ("neural network", 1.5), ("deep learning", 1.5)
    ],
    
    "Cyber Security": [
        ("security", 1), ("malware", 2), ("phishing", 2), ("intrusion", 2),
        ("attack", 1), ("threat", 1), ("encryption", 1.5), ("vulnerability", 1.5),
        ("penetration", 2), ("cyberattack", 2), ("breach", 1.5)
    ],
    
    "Data Mining": [
        ("clustering", 2), ("association rules", 2), ("frequent patterns", 2),
        ("data mining", 2), ("kmeans", 1.5), ("dbscan", 1.5), ("classification", 1),
        ("pattern discovery", 2), ("anomaly detection", 1.5)
    ]
}


def classify_domain(text: str, confidence_threshold: float = 0) -> Tuple[str, Dict[str, float]]:
    """
    Classify research domain using keyword matching with weighted scoring.
    
    Args:
        text: Input research paper text
        confidence_threshold: Minimum score to classify a domain
    
    Returns:
        Tuple of (domain_name, scores_dict)
    """
    if not text or len(text) < 50:
        logger.warning("Text too short for domain classification")
        return "General Research", {}
    
    try:
        text_lower = text.lower()
        scores = {}
        
        # Calculate weighted scores for each domain
        for domain, keywords in DOMAIN_KEYWORDS.items():
            score = 0.0
            for keyword, weight in keywords:
                # Count occurrences using word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(keyword) + r'\b'
                count = len(re.findall(pattern, text_lower))
                score += count * weight
            
            scores[domain] = score
        
        # Find the domain with highest score
        if not scores or all(v == 0 for v in scores.values()):
            logger.info("No domain keywords found, classifying as General Research")
            return "General Research", scores
        
        best_domain = max(scores, key=scores.get)
        best_score = scores[best_domain]
        
        # Check if confidence is above threshold
        if best_score <= confidence_threshold:
            logger.info(f"Low confidence for any domain (score: {best_score})")
            return "General Research", scores
        
        logger.info(f"✅ Classified as {best_domain} (score: {best_score:.1f})")
        return best_domain, scores
        
    except Exception as e:
        logger.error(f"Error classifying domain: {e}")
        return "General Research", {}


def classify_domain_simple(text: str) -> str:
    """Simple wrapper for backward compatibility"""
    domain, _ = classify_domain(text)
    return domain
