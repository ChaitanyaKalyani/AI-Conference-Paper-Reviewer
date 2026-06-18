"""
Problem statement extraction module
"""

from modules.llm_utils import safe_llm_call, validate_text_input
import logging

logger = logging.getLogger(__name__)

def extract_problem_statement(text):
    """
    Extract the research problem statement from the paper
    
    Args:
        text: Full paper text
    
    Returns:
        str: Concise problem statement
    """
    try:
        validate_text_input(text, min_length=100)
        
        prompt = f"""
Extract ONLY the core research problem from this paper.

Guidelines:
- Maximum 4-5 lines
- Clearly state what problem is being addressed
- Explain why this problem is important
- Do NOT include methodology or results
- Use clear, professional language

Paper excerpt:
{text[:5000]}
"""
        
        result = safe_llm_call(prompt)
        return result
        
    except Exception as e:
        logger.error(f"Error extracting problem statement: {str(e)}")
        return f"Error: {str(e)}"
