import re
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define recommendation patterns with confidence weights
RECOMMENDATION_PATTERNS = {
    "Major Revision": [
        (r"major revision", 1.0),
        (r"major changes", 0.8),
        (r"significant changes", 0.7),
        (r"major concerns", 0.6)
    ],
    
    "Minor Revision": [
        (r"minor revision", 1.0),
        (r"minor changes", 0.8),
        (r"small improvements", 0.7),
        (r"minor issues", 0.6),
        (r"minor corrections", 0.8)
    ],
    
    "Reject": [
        (r"\breject\b", 1.0),
        (r"rejected", 0.9),
        (r"not suitable", 0.7),
        (r"not acceptable", 0.7),
        (r"cannot accept", 0.8),
        (r"should not be published", 0.8)
    ],
    
    "Accept": [
        (r"\baccept\b", 1.0),
        (r"accepted", 0.9),
        (r"acceptable", 0.8),
        (r"publication", 0.6),
        (r"recommend acceptance", 1.0),
        (r"ready to publish", 0.9)
    ]
}


def extract_recommendation(review: str, confidence_threshold: float = 0.5) -> Tuple[str, float]:
    """
    Extract recommendation from review text with confidence score.
    
    Args:
        review: The review text
        confidence_threshold: Minimum confidence to return a recommendation
    
    Returns:
        Tuple of (recommendation, confidence_score)
    """
    if not review:
        logger.warning("Empty review text provided")
        return "Not Found", 0.0
    
    try:
        review_lower = review.lower()
        scores = {}
        
        # Calculate confidence for each recommendation
        for recommendation, patterns in RECOMMENDATION_PATTERNS.items():
            confidence = 0.0
            matches_found = False
            
            for pattern, weight in patterns:
                if re.search(pattern, review_lower):
                    confidence = max(confidence, weight)
                    matches_found = True
            
            if matches_found:
                scores[recommendation] = confidence
        
        # Find the recommendation with highest confidence
        if not scores or max(scores.values()) < confidence_threshold:
            logger.info("Low confidence for recommendation extraction")
            return "Not Found", 0.0
        
        best_recommendation = max(scores, key=scores.get)
        best_confidence = scores[best_recommendation]
        
        logger.info(f"✅ Extracted recommendation: {best_recommendation} (confidence: {best_confidence:.2f})")
        return best_recommendation, best_confidence
        
    except Exception as e:
        logger.error(f"Error extracting recommendation: {e}")
        return "Not Found", 0.0


def extract_recommendation_simple(review: str) -> str:
    """Simple wrapper for backward compatibility"""
    recommendation, _ = extract_recommendation(review)
    return recommendation
