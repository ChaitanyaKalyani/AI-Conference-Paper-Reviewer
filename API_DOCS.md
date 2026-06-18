# 📚 API Documentation

Complete API reference for the Conference Paper Reviewer modules.

## Table of Contents
1. [LLM Utilities](#llm-utilities)
2. [Review Generation](#review-generation)
3. [Text Analysis](#text-analysis)
4. [Report Generation](#report-generation)
5. [Paper Search](#paper-search)
6. [Entity & Domain Analysis](#entity--domain-analysis)

---

## LLM Utilities

### Module: `modules/llm_utils.py`

Core LLM client with error handling, retry logic, and input validation.

#### `get_llm_client()`
Initialize or retrieve the OpenAI LLM client (singleton pattern).

```python
from modules.llm_utils import get_llm_client

client = get_llm_client()
# Returns initialized OpenAI client
```

**Returns**: `openai.OpenAI` - Configured LLM client

---

#### `retry_with_backoff(max_retries=3)`
Decorator for automatic retry with exponential backoff.

```python
from modules.llm_utils import retry_with_backoff

@retry_with_backoff(max_retries=3)
def my_function():
    # Function with automatic retry on failure
    pass
```

**Parameters**:
- `max_retries` (int): Maximum retry attempts

**Returns**: Decorated function with retry logic

---

#### `safe_llm_call(prompt, system_prompt="", temperature=0, top_p=0.1, max_tokens=2000)`
Unified LLM interface with comprehensive error handling.

```python
from modules.llm_utils import safe_llm_call

result = safe_llm_call(
    prompt="Analyze this paper",
    system_prompt="You are a peer reviewer",
    temperature=0,
    max_tokens=1500
)
```

**Parameters**:
- `prompt` (str): User prompt
- `system_prompt` (str): System context
- `temperature` (float): 0-2, controls randomness
- `top_p` (float): Nucleus sampling parameter
- `max_tokens` (int): Maximum response length

**Returns**: `str` - LLM response

**Raises**: `ValueError` - For invalid inputs or API errors

---

#### `validate_text_input(text, min_length=50, max_length=50000)`
Validate user text input.

```python
from modules.llm_utils import validate_text_input

try:
    validate_text_input(text, min_length=100, max_length=30000)
except ValueError as e:
    print(f"Invalid input: {e}")
```

**Parameters**:
- `text` (str): Text to validate
- `min_length` (int): Minimum allowed length
- `max_length` (int): Maximum allowed length

**Returns**: `bool` - True if valid

**Raises**: `ValueError` - If validation fails

---

#### `sanitize_for_pdf(text)`
Clean text for PDF generation (handle Unicode and special characters).

```python
from modules.llm_utils import sanitize_for_pdf

clean_text = sanitize_for_pdf(original_text)
```

**Parameters**:
- `text` (str): Text to sanitize

**Returns**: `str` - Cleaned text safe for PDF

---

## Review Generation

### Module: `modules/reviewer.py`

Generate IEEE-style conference reviews with scoring.

#### `generate_review(sections, retrieved_context="")`
Generate a comprehensive peer review.

```python
from modules.reviewer import generate_review

sections = {
    "abstract": "...",
    "introduction": "...",
    "methodology": "...",
    "results": "...",
    "conclusion": "..."
}

review = generate_review(sections, retrieved_context="Related work...")
```

**Parameters**:
- `sections` (dict): Paper sections {key: text}
- `retrieved_context` (str): Related papers context

**Returns**: `str` - Formatted review with scores

**Review Format**:
```
Novelty Score: X/10
Technical Quality Score: X/10
Clarity Score: X/10
Significance Score: X/10

Detailed Review:
[Review text with reasoning]

Final Recommendation: [Accept/Minor Revision/Major Revision/Reject]
```

---

## Text Analysis

### Module: `modules/summarizer.py`

Generate paper summaries.

#### `generate_summary(sections)`
Create executive summary of paper.

```python
from modules.summarizer import generate_summary

sections = {"introduction": "...", "methodology": "..."}
summary = generate_summary(sections)
```

**Parameters**:
- `sections` (dict): Paper sections

**Returns**: `str` - Executive summary

---

### Module: `modules/problem_extractor.py`

Extract research problem statements.

#### `extract_problem_statement(text)`
Extract the research problem from text.

```python
from modules.problem_extractor import extract_problem_statement

problem = extract_problem_statement(paper_text)
```

**Parameters**:
- `text` (str): Input text

**Returns**: `str` - Problem statement (4-5 lines)

---

### Module: `modules/contribution_extractor.py`

Extract research contributions.

#### `extract_contributions(text)`
Extract key contributions from paper.

```python
from modules.contribution_extractor import extract_contributions

contributions = extract_contributions(paper_text)
```

**Parameters**:
- `text` (str): Input text

**Returns**: `str` - Bullet-point contributions (3-5 items)

---

## Report Generation

### Module: `modules/report_generator.py`

Generate professional reports in PDF and text formats.

#### `generate_pdf_report(filename, review, recommendation, scores=None)`
Create professional PDF report.

```python
from modules.report_generator import generate_pdf_report

scores = {
    "novelty": 8,
    "technical": 7,
    "clarity": 9,
    "significance": 8
}

generate_pdf_report(
    "review_report.pdf",
    review_text,
    "Accept",
    scores=scores
)
```

**Parameters**:
- `filename` (str): Output PDF filename
- `review` (str): Review text
- `recommendation` (str): Recommendation decision
- `scores` (dict): Optional score dictionary

**Returns**: `None` - Writes PDF file

**Raises**: `Exception` - If PDF generation fails

---

#### `generate_text_report(review, recommendation, scores=None, metadata=None)`
Create structured text report.

```python
from modules.report_generator import generate_text_report

metadata = {"Pages": 12, "Authors": 3}
text_report = generate_text_report(
    review,
    recommendation,
    scores=scores,
    metadata=metadata
)
```

**Parameters**:
- `review` (str): Review text
- `recommendation` (str): Recommendation
- `scores` (dict): Score dictionary
- `metadata` (dict): Optional metadata

**Returns**: `str` - Formatted text report

---

### Module: `modules/score_parser.py`

Extract numerical scores from reviews.

#### `extract_score(review_text, score_name)`
Extract a specific score value.

```python
from modules.score_parser import extract_score

novelty = extract_score(review_text, "Novelty Score")
technical = extract_score(review_text, "Technical Quality Score")
```

**Parameters**:
- `review_text` (str): Review text containing scores
- `score_name` (str): Score identifier

**Returns**: `int` - Score value (0-10)

---

#### `extract_all_scores(review_text)`
Extract all scores from review.

```python
from modules.score_parser import extract_all_scores

scores = extract_all_scores(review_text)
# Returns: {"novelty": 8, "technical": 7, "clarity": 9, "significance": 8}
```

**Parameters**:
- `review_text` (str): Review text

**Returns**: `dict` - All scores

---

### Module: `modules/recommendation_parser.py`

Extract recommendation from reviews.

#### `extract_recommendation_simple(review)`
Extract recommendation decision.

```python
from modules.recommendation_parser import extract_recommendation_simple

recommendation = extract_recommendation_simple(review_text)
# Returns: "Accept", "Minor Revision", "Major Revision", or "Reject"
```

**Parameters**:
- `review` (str): Review text

**Returns**: `str` - Recommendation decision

---

#### `extract_recommendation(review, confidence_threshold=0.5)`
Extract recommendation with confidence score.

```python
from modules.recommendation_parser import extract_recommendation

recommendation, confidence = extract_recommendation(review_text)
# Returns: ("Accept", 0.95)
```

**Parameters**:
- `review` (str): Review text
- `confidence_threshold` (float): Minimum confidence

**Returns**: `Tuple[str, float]` - (recommendation, confidence_score)

---

## Paper Search

### Module: `modules/arxiv_retriever.py`

Search arXiv for related papers.

#### `search_arxiv(query, max_results=5)`
Search arXiv for papers.

```python
from modules.arxiv_retriever import search_arxiv

papers = search_arxiv("transformer architecture", max_results=10)
# Returns list of papers with title, summary, URL, authors
```

**Parameters**:
- `query` (str): Search query
- `max_results` (int): Maximum results (1-100)

**Returns**: `List[dict]` - Papers with fields:
  - `title` (str): Paper title
  - `summary` (str): Paper abstract
  - `url` (str): arXiv URL
  - `authors` (str): Comma-separated authors

---

### Module: `modules/rag_ranker.py`

Rank papers by semantic similarity.

#### `rank_papers(uploaded_text, papers, top_k=3)`
Rank papers by relevance.

```python
from modules.rag_ranker import rank_papers

ranked = rank_papers(
    uploaded_text=paper_text,
    papers=paper_list,
    top_k=5
)
```

**Parameters**:
- `uploaded_text` (str): Reference text
- `papers` (List[dict]): Papers with 'summary' field
- `top_k` (int): Number of top papers

**Returns**: `List[dict]` - Ranked papers

---

### Module: `modules/rag_engine.py`

FAISS-based similarity search engine.

#### `load_dataset_papers(dataset_folder="dataset")`
Load papers from local dataset.

```python
from modules.rag_engine import load_dataset_papers

papers = load_dataset_papers("dataset")
```

**Parameters**:
- `dataset_folder` (str): Path to dataset folder

**Returns**: `List[dict]` - Papers with filename and text

---

#### `create_embeddings(papers)`
Create embeddings for papers.

```python
from modules.rag_engine import create_embeddings

embeddings = create_embeddings(papers)
```

**Parameters**:
- `papers` (List[dict]): Papers list

**Returns**: `np.ndarray` - Embedding vectors

---

#### `create_faiss_index(embeddings)`
Create FAISS index from embeddings.

```python
from modules.rag_engine import create_faiss_index

index = create_faiss_index(embeddings)
```

**Parameters**:
- `embeddings` (np.ndarray): Embedding array

**Returns**: `faiss.IndexFlatL2` - FAISS index

---

#### `find_similar_papers(uploaded_text, papers, index, top_k=3)`
Find similar papers using FAISS.

```python
from modules.rag_engine import find_similar_papers

similar = find_similar_papers(
    uploaded_text=paper_text,
    papers=papers,
    index=faiss_index,
    top_k=5
)
```

**Parameters**:
- `uploaded_text` (str): Query text
- `papers` (List[dict]): Papers list
- `index` (faiss.Index): FAISS index
- `top_k` (int): Number of results

**Returns**: `List[str]` - Similar paper filenames

---

## Entity & Domain Analysis

### Module: `modules/entity_extractor.py`

Extract named entities from text.

#### `extract_entities(text, max_entities=20)`
Extract named entities.

```python
from modules.entity_extractor import extract_entities

entities = extract_entities(paper_text, max_entities=25)
```

**Parameters**:
- `text` (str): Input text
- `max_entities` (int): Maximum entities to return

**Returns**: `List[str]` - Extracted entities

---

### Module: `modules/domain_classifier.py`

Classify research domains.

#### `classify_domain_simple(text)`
Classify research domain.

```python
from modules.domain_classifier import classify_domain_simple

domain = classify_domain_simple(paper_text)
# Returns: "Natural Language Processing", "Computer Vision", etc.
```

**Parameters**:
- `text` (str): Paper text

**Returns**: `str` - Domain name

---

#### `classify_domain(text, confidence_threshold=0)`
Classify with confidence scores.

```python
from modules.domain_classifier import classify_domain

domain, scores = classify_domain(paper_text)
# Returns: ("NLP", {"NLP": 25.5, "CV": 5.0, ...})
```

**Parameters**:
- `text` (str): Paper text
- `confidence_threshold` (float): Minimum threshold

**Returns**: `Tuple[str, dict]` - (domain, scores)

---

## Error Handling

All modules include comprehensive error handling:

```python
from modules.llm_utils import safe_llm_call

try:
    result = safe_llm_call(prompt)
except ValueError as e:
    print(f"Invalid input: {e}")
except Exception as e:
    print(f"API error: {e}")
```

Common exceptions:
- `ValueError`: Invalid inputs
- `TimeoutError`: API timeout
- `APIError`: OpenRouter API error
- `ConnectionError`: Network error

---

## Logging

Enable debug logging:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

Log levels:
- `DEBUG`: Detailed execution flow
- `INFO`: General information
- `WARNING`: Warning messages
- `ERROR`: Error messages

---

## Examples

### Complete Review Generation Example

```python
from modules.arxiv_retriever import search_arxiv
from modules.reviewer import generate_review
from modules.report_generator import generate_pdf_report
from modules.score_parser import extract_all_scores
from modules.recommendation_parser import extract_recommendation_simple

# Extract sections from uploaded paper
sections = {
    "abstract": "...",
    "introduction": "...",
    "methodology": "...",
    "results": "...",
    "conclusion": "..."
}

# Get related papers
query = "transformer attention mechanism"
related_papers = search_arxiv(query, max_results=5)
context = "\n\n".join([f"{p['title']}\n{p['summary']}" for p in related_papers])

# Generate review
review = generate_review(sections, context)

# Extract scores
scores = extract_all_scores(review)

# Get recommendation
recommendation = extract_recommendation_simple(review)

# Generate PDF report
generate_pdf_report("review.pdf", review, recommendation, scores)

print(f"Review generated successfully!")
print(f"Scores: {scores}")
print(f"Recommendation: {recommendation}")
```

---

## Version History

- **v1.0.0** (2025-01-15)
  - Initial release
  - Core modules functional
  - Production-ready

---

## Support

For API questions or issues:
1. Check examples above
2. Review module docstrings
3. Check GitHub issues
4. Open a new issue with details

---

**Last Updated**: January 2025
**API Version**: 1.0.0
