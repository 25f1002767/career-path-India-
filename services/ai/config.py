import os
import logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

logger = logging.getLogger("mpath.ai.config")

# Model Configuration (Centralized & Configurable via environment)
AI_MODEL = os.getenv("OPENAI_MODEL", os.getenv("AI_MODEL", "gpt-4o"))
AI_REASONING_MODEL = os.getenv("OPENAI_REASONING_MODEL", os.getenv("AI_REASONING_MODEL", "o1"))
AI_FAST_MODEL = os.getenv("OPENAI_FAST_MODEL", os.getenv("AI_FAST_MODEL", "gpt-4o-mini"))

# Gemini Fallback Models
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
GEMINI_FAST_MODEL = os.getenv("GEMINI_FAST_MODEL", "gemini-3.8-flash")

# API Keys (Kept server-side only)
OPENAI_API_KEY = (os.getenv("OPENAI_API_KEY") or "").strip()
GEMINI_API_KEY = (os.getenv("GEMINI_API_KEY") or "").strip()

# Clients
openai_client = None
if OPENAI_API_KEY:
    try:
        from openai import OpenAI
        openai_client = OpenAI(
            api_key=OPENAI_API_KEY,
            timeout=30.0,
            max_retries=2
        )
        logger.info("OpenAI client initialized successfully with model: %s", AI_MODEL)
    except Exception as e:
        logger.error("Failed to initialize OpenAI client: %s", e)
        openai_client = None

gemini_client = None
if GEMINI_API_KEY:
    try:
        from google import genai
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        logger.info("Google GenAI client initialized successfully")
    except Exception as e:
        logger.error("Failed to initialize Gemini client: %s", e)
        gemini_client = None


def get_available_provider():
    """
    Returns the primary active provider:
    'openai' -> if OpenAI client is active
    'gemini' -> if Gemini client is active
    'local' -> grounded MPath database fallback
    """
    if openai_client:
        return "openai"
    if gemini_client:
        return "gemini"
    return "local"
