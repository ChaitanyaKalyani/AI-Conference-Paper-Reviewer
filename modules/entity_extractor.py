import logging
import spacy
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model cache for lazy loading
_nlp_cache = None

def get_spacy_model():
    """Get or initialize the spaCy model (lazy loading)"""
    global _nlp_cache
    if _nlp_cache is None:
        logger.info("Loading spaCy model (this happens once)...")
        _nlp_cache = spacy.load("en_core_web_sm")
        logger.info("✅ spaCy model loaded")
    return _nlp_cache


def extract_entities(text: str, max_entities: int = 20) -> List[str]:
    """
    Extract named entities from text using spaCy.
    
    Args:
        text: Input text to extract entities from
        max_entities: Maximum number of entities to return
    
    Returns:
        List of unique, filtered entities
    """
    if not text:
        logger.warning("Empty text provided for entity extraction")
        return []
    
    try:
        nlp = get_spacy_model()
        doc = nlp(text[:10000])
        
        # Set of common noise entities to filter
        bad_entities = {
            "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
            "tan", "pan", "yue", "feinashl", "roughly 100", "al.",
            "a", "the", "an", "and", "or", "in", "is", "are", "be", "been"
        }
        
        entities = []
        seen = set()  # Track seen entities for uniqueness
        
        for ent in doc.ents:
            entity = ent.text.strip()
            
            # Skip if already seen
            if entity in seen:
                continue
            
            # Skip noise entities
            if entity.lower() in bad_entities:
                continue
            
            # Skip short entities
            if len(entity) < 3:
                continue
            
            # Skip pure numbers
            if entity.isdigit():
                continue
            
            # Skip entries with too many digits (likely dates/numbers)
            if any(char.isdigit() for char in entity) and len(entity) < 10:
                continue
            
            # Skip percentage-like entities
            if "%" in entity:
                continue
            
            # This is a valid entity
            seen.add(entity)
            entities.append(entity)
            
            # Stop if we've reached max entities
            if len(entities) >= max_entities:
                break
        
        logger.info(f"✅ Extracted {len(entities)} entities")
        return entities
        
    except Exception as e:
        logger.error(f"Error extracting entities: {e}")
        return []
