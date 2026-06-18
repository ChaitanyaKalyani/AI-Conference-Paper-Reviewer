import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# For development/testing without API key, show warning
if not OPENROUTER_API_KEY or OPENROUTER_API_KEY.startswith("your-openrouter-api-key"):
    print("⚠️  WARNING: OPENROUTER_API_KEY not configured properly. Some features will not work.")
    print("Please set OPENROUTER_API_KEY in your .env file")
    OPENROUTER_API_KEY = "dummy_key_for_testing"

# LLM Configuration
LLM_MODEL = os.getenv("LLM_MODEL", "openai/gpt-oss-20b:free")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0"))
LLM_TOP_P = float(os.getenv("LLM_TOP_P", "0.1"))

# Application Configuration
MAX_PDF_PAGES = int(os.getenv("MAX_PDF_PAGES", "100"))
MAX_TEXT_LENGTH = int(os.getenv("MAX_TEXT_LENGTH", "50000"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "30"))
