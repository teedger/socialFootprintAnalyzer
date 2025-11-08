"""
Configuration file for Social Footprint Analyzer
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID", "")
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
    TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "SocialFootprintAnalyzer/1.0")

    # Application Settings
    DEBUG = os.getenv("DEBUG", "True") == "True"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))

    # Analysis Settings
    MAX_SEARCH_RESULTS = 50
    SENTIMENT_THRESHOLD_POSITIVE = 0.1
    SENTIMENT_THRESHOLD_NEGATIVE = -0.1

    @classmethod
    def validate(cls):
        """Validate that required API keys are set"""
        warnings = []
        if not cls.OPENAI_API_KEY:
            warnings.append("OPENAI_API_KEY not set - AI analysis will be limited")
        if not cls.GOOGLE_API_KEY:
            warnings.append("GOOGLE_API_KEY not set - Google search will be disabled")
        if not cls.NEWSAPI_KEY:
            warnings.append("NEWSAPI_KEY not set - News search will be disabled")

        return warnings
