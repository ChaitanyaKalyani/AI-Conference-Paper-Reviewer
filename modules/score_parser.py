"""
Score extraction from review text
"""

import re
import logging

logger = logging.getLogger(__name__)

def extract_score(review_text, score_name):
    """
    Extract a numerical score from review text
    
    Args:
        review_text: The review text containing scores
        score_name: Name of the score to extract (e.g., "Novelty Score")
    
    Returns:
        int: Score value 0-10, defaults to 0 if not found
    """
    try:
        if not review_text or not score_name:
            return 0
        
        # Remove asterisks and extra whitespace
        review_text = review_text.replace("*", "").strip()
        
        # Pattern to match "Score Name: number" or "Score Name: number/10"
        pattern = rf"{re.escape(score_name)}\s*:?\s*(\d+)"
        match = re.search(pattern, review_text, re.IGNORECASE)
        
        if match:
            score = int(match.group(1))
            # Ensure score is in valid range
            return max(0, min(10, score))
        
        logger.warning(f"Score '{score_name}' not found in review text")
        return 0
        
    except (ValueError, AttributeError) as e:
        logger.error(f"Error extracting score '{score_name}': {str(e)}")
        return 0
    except Exception as e:
        logger.error(f"Unexpected error in extract_score: {str(e)}")
        return 0

def extract_all_scores(review_text):
    """
    Extract all scores at once
    
    Args:
        review_text: Review containing all scores
    
    Returns:
        dict: Dictionary with score names as keys
    """
    score_names = [
        "Novelty Score",
        "Technical Quality Score",
        "Clarity Score",
        "Significance Score"
    ]
    
    return {
        name: extract_score(review_text, name)
        for name in score_names
    }
