"""
Conference paper reviewer module - Generates detailed reviews with scores
"""

from modules.llm_utils import safe_llm_call, validate_text_input
import logging

logger = logging.getLogger(__name__)

def generate_review(sections, retrieved_context=""):
    """
    Generate a detailed conference review with scoring
    
    Args:
        sections: dict of paper sections (Abstract, Introduction, etc.)
        retrieved_context: optional context from related papers
    
    Returns:
        str: Review with scores and recommendation
    """
    try:
        # Validate input
        paper_content = " ".join(str(v) for v in sections.values() if v)
        validate_text_input(paper_content, min_length=100)
        
        prompt = f"""
You are an expert IEEE conference reviewer with 15+ years of experience.

EVALUATION CRITERIA:
Evaluate the paper on these scores (0-10 scale):
- Novelty Score: How novel/original is the research?
- Technical Quality Score: How rigorous is the methodology?
- Clarity Score: How well is the paper written?
- Significance Score: What's the impact of this work?

INSTRUCTIONS:
1. Provide scores as integers only (e.g., "Novelty Score: 7")
2. Be deterministic - same paper should get same scores
3. Ignore formatting/OCR errors - evaluate research content only
4. Provide final recommendation: Accept / Minor Revision / Major Revision / Reject

FORMAT YOUR RESPONSE AS:

Novelty Score: [0-10]
Technical Quality Score: [0-10]
Clarity Score: [0-10]
Significance Score: [0-10]

Final Recommendation: [Accept/Minor Revision/Major Revision/Reject]

Detailed Review:

1. Summary of the Paper
2. Strengths (3-5 points)
3. Weaknesses (3-5 points)
4. Technical Soundness
5. Suggestions for Improvement
6. Questions for Authors

--- CONTEXT FROM RELATED RESEARCH ---
{retrieved_context if retrieved_context else "No related papers retrieved"}

--- PAPER CONTENT ---
ABSTRACT:
{sections.get('Abstract', 'Not found')[:2000]}

INTRODUCTION:
{sections.get('Introduction', 'Not found')[:2000]}

METHODOLOGY:
{sections.get('Methodology', 'Not found')[:2000]}

RESULTS:
{sections.get('Results', 'Not found')[:2000]}

CONCLUSION:
{sections.get('Conclusion', 'Not found')[:2000]}
"""
        
        result = safe_llm_call(prompt)
        return result
        
    except Exception as e:
        logger.error(f"Error generating review: {str(e)}")
        return f"Error generating review: {str(e)}"
