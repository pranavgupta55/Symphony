"""
Configuration module for Symphony AI Backend
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""

    # API Keys
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./symphony.db")

    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:5173",  # Vite default
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    # File Upload
    MAX_AUDIO_SIZE: int = int(os.getenv("MAX_AUDIO_SIZE", "100")) * 1024 * 1024  # MB to bytes
    MAX_CHART_SIZE: int = int(os.getenv("MAX_CHART_SIZE", "10")) * 1024 * 1024   # MB to bytes

    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    AUDIO_DIR: Path = UPLOAD_DIR / "audio"
    CHARTS_DIR: Path = UPLOAD_DIR / "charts"

    # Processing
    ENABLE_CACHE: bool = os.getenv("ENABLE_CACHE", "true").lower() == "true"
    MAX_CONCURRENT_JOBS: int = int(os.getenv("MAX_CONCURRENT_JOBS", "5"))

    # Audio Processing
    SAMPLE_RATE: int = 16000
    N_MFCC: int = 20
    HOP_LENGTH: int = 512

    # Model names
    FINBERT_MODEL: str = "ProsusAI/finbert"

    # Claude AI Configuration
    CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929")
    CLAUDE_MAX_TOKENS: int = int(os.getenv("CLAUDE_MAX_TOKENS", "4096"))
    CLAUDE_TEMPERATURE: float = float(os.getenv("CLAUDE_TEMPERATURE", "0.7"))
    ENABLE_PROMPT_CACHING: bool = os.getenv("ENABLE_PROMPT_CACHING", "true").lower() == "true"

    def __init__(self):
        """Create necessary directories"""
        self.UPLOAD_DIR.mkdir(exist_ok=True)
        self.AUDIO_DIR.mkdir(exist_ok=True)
        self.CHARTS_DIR.mkdir(exist_ok=True)


settings = Settings()
