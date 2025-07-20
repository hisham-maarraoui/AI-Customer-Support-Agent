from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    # Google Gemini Configuration
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    
    # Pinecone Configuration
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY", "")
    pinecone_environment: str = os.getenv("PINECONE_ENVIRONMENT", "")
    pinecone_index_name: str = os.getenv("PINECONE_INDEX_NAME", "apple-support")
    
    # Vapi Configuration
    vapi_api_key: Optional[str] = os.getenv("VAPI_API_KEY")
    vapi_public_key: Optional[str] = os.getenv("VAPI_PUBLIC_KEY")
    
    # Application Configuration
    app_name: str = os.getenv("APP_NAME", "Apple Support AI Agent")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Rate Limiting
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    # Model Configuration
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "models/embedding-001")
    
    # Vector Database Configuration
    vector_dimension: int = int(os.getenv("VECTOR_DIMENSION", "768"))
    vector_metric: str = os.getenv("VECTOR_METRIC", "cosine")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings() 