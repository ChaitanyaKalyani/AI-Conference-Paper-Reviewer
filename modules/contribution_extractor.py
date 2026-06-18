"""
Research contributions extraction module
"""

from modules.llm_utils import safe_llm_call, validate_text_input
import logging

logger = logging.getLogger(__name__)

def extract_contributions(text):
    """
    Extract main research contributions from the paper
    
    Args:
        text: Full paper text
    
    Returns:
        str: List of key contributions
    """
    try:
        validate_text_input(text, min_length=100)
        
        prompt = f"""
Extract and list the main research contributions from this paper.

Format as bullet points with these guidelines:
- List 3-5 key contributions
- Start each with an action verb (e.g., "Proposes", "Develops", "Introduces")
- Keep each contribution to 1-2 lines
- Focus ONLY on research contributions
- Avoid problem statements or conclusions

Paper excerpt:
{text[:5000]}
"""
        
        result = safe_llm_call(prompt)
        return result
        
    except Exception as e:
        logger.error(f"Error extracting contributions: {str(e)}")
        return f"Error: {str(e)}"
