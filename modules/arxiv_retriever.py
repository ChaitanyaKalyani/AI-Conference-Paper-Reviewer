import logging
import feedparser
import requests
from typing import List, Dict
from urllib.parse import urlencode

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def search_arxiv(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Search arXiv for papers matching the query.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
    
    Returns:
        List of paper dictionaries with title, summary, and URL
    """
    if not query or not query.strip():
        logger.warning("Empty query provided")
        return []
    
    if max_results < 1 or max_results > 100:
        logger.warning(f"Invalid max_results: {max_results}, using default of 5")
        max_results = 5
    
    try:
        params = urlencode({
            "search_query": query.strip(),
            "start": 0,
            "max_results": max_results,
            "sortBy": "relevance",
            "sortOrder": "descending",
        })
        response = requests.get(
            f"https://export.arxiv.org/api/query?{params}",
            timeout=20,
            headers={"User-Agent": "ConferencePaperReviewer/1.0"},
        )
        response.raise_for_status()
        feed = feedparser.parse(response.text)
        
        papers = []
        for entry in feed.entries:
            try:
                authors = entry.get("authors", [])
                papers.append({
                    "title": entry.get("title", "").strip(),
                    "summary": entry.get("summary", "").strip(),
                    "url": entry.get("id", ""),
                    "authors": ", ".join(author.get("name", "") for author in authors[:3])
                })
            except Exception as e:
                logger.warning(f"Error processing result: {e}")
                continue
        
        logger.info(f"✅ Found {len(papers)} papers on arXiv")
        return papers
        
    except Exception as e:
        logger.error(f"Error searching arXiv: {e}")
        return []
