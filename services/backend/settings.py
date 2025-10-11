import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
root_dir = Path(__file__).parent
dotenv_path = root_dir / ".env"
load_dotenv(dotenv_path=dotenv_path)

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
# Use PORT environment variable (common in cloud deployments) or fallback to API_PORT or 8000
API_PORT = int(os.getenv("PORT", os.getenv("API_PORT", "8000")))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "europe-west1")
GOOGLE_GENAI_USE_VERTEXAI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "True")

# Ollama Configuration
OLLAMA_API_BASE = os.getenv(
    "OLLAMA_API_BASE", "https://ollama-153939933605.europe-west1.run.app"
)
GEMMA_MODEL_NAME = os.getenv("GEMMA_MODEL_NAME", "gemma3:12b")

# Image Processing Configuration
MAX_IMAGE_SIZE = (1024, 1024)
ALLOWED_IMAGE_FORMATS = ["JPEG", "PNG", "WEBP"]
