"""
Shared utilities and LLM client initialization
Prevents code duplication and ensures consistent error handling
"""

import os
import logging
import time
from functools import wraps
from openai import OpenAI, APIError, APIConnectionError
from config import OPENROUTER_API_KEY, LLM_MODEL, LLM_TEMPERATURE, LLM_TOP_P, MAX_RETRIES

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client (singleton pattern)
_client = None

def get_llm_client():
    """Get or create OpenAI client (singleton)"""
    global _client
    if _client is None:
        _client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY
        )
    return _client

def retry_with_backoff(max_retries=MAX_RETRIES, backoff_factor=2):
    """Decorator for retrying failed API calls with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (APIError, APIConnectionError) as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Max retries reached for {func.__name__}: {str(e)}")
                        raise
                    wait_time = backoff_factor ** attempt
                    logger.warning(f"Retry attempt {attempt + 1}/{max_retries} for {func.__name__} after {wait_time}s")
                    time.sleep(wait_time)
                except Exception as e:
                    logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
                    raise
        return wrapper
    return decorator

def safe_llm_call(prompt, model=LLM_MODEL, temperature=LLM_TEMPERATURE, top_p=LLM_TOP_P):
    """Safely call LLM with error handling and input validation"""
    try:
        if not prompt or len(prompt) == 0:
            raise ValueError("Prompt cannot be empty")
        
        if len(prompt) > 100000:
            logger.warning(f"Prompt length {len(prompt)} exceeds recommended limit, truncating...")
            prompt = prompt[:100000]
        
        client = get_llm_client()
        
        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            top_p=top_p,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content
        
    except ValueError as e:
        logger.error(f"Input validation error: {str(e)}")
        return f"Input Error: {str(e)}"
    except APIError as e:
        logger.error(f"API Error: {str(e)}")
        return f"API Error: Please try again later"
    except Exception as e:
        logger.error(f"Unexpected error in LLM call: {str(e)}")
        return f"Error: {str(e)}"

def validate_text_input(text, min_length=10, max_length=50000):
    """Validate text input for safety and size"""
    if not text or len(text.strip()) < min_length:
        raise ValueError(f"Text must be at least {min_length} characters")
    if len(text) > max_length:
        logger.warning(f"Text truncated from {len(text)} to {max_length} characters")
        return text[:max_length]
    return text

def sanitize_for_pdf(text):
    """Sanitize text for PDF generation"""
    # Remove problematic unicode characters
    replacements = {
        "\u25a0": "*",
        "\u2022": "*",
        "\u2013": "-",
        "\u2014": "-",
        "\u201c": '"',
        "\u201d": '"',
        "\u2018": "'",
        "\u2019": "'",
    }
    for source, replacement in replacements.items():
        text = text.replace(source, replacement)
    
    # Remove markdown formatting
    text = text.replace("**", "")
    text = text.replace("###", "")
    text = text.replace("##", "")
    text = text.replace("#", "")
    
    return text
