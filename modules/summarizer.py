"""
Paper summarization module - Generates executive summaries
"""

from modules.llm_utils import safe_llm_call, validate_text_input
import logging

logger = logging.getLogger(__name__)

def generate_summary(sections):
    """
    Generate a comprehensive summary of the research paper
    
    Args:
        sections: dict of paper sections
    
    Returns:
        str: Executive summary with key points
    """
    try:
        # Validate input
        paper_content = " ".join(str(v) for v in sections.values() if v)
        validate_text_input(paper_content, min_length=100)
        
        prompt = f"""
You are an expert research paper analyst specializing in academic summaries.

Generate a professional executive summary with these sections:

1. RESEARCH OBJECTIVE (2-3 lines)
   What problem does this paper address?

2. METHODOLOGY (3-4 lines)
   How did the authors approach this problem?

3. KEY CONTRIBUTIONS (4-5 bullet points)
   What are the main contributions?

4. MAIN FINDINGS (3-4 lines)
   What are the significant results?

5. IMPLICATIONS (2-3 lines)
   What's the broader impact?

6. CONCLUSION (2 lines)
   Final summary

--- PAPER CONTENT ---
ABSTRACT:
{sections.get('Abstract', 'Not found')[:1500]}

INTRODUCTION:
{sections.get('Introduction', 'Not found')[:1500]}

METHODOLOGY:
{sections.get('Methodology', 'Not found')[:1500]}

RESULTS:
{sections.get('Results', 'Not found')[:1500]}

CONCLUSION:
{sections.get('Conclusion', 'Not found')[:1500]}
"""
        
        result = safe_llm_call(prompt)
        return result
        
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        return f"Error generating summary: {str(e)}"
