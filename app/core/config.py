import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Arxiv Sanity Modern"
    PROJECT_VERSION: str = "0.1.0"
    
    # Storage paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    DB_PATH: str = os.path.join(DATA_DIR, "papers.db")
    
    # Arxiv Settings
    ARXIV_QUERY_INTERVAL_HOURS: int = 24
    
    class Config:
        case_sensitive = True

settings = Settings()

# Ensure data directory exists
os.makedirs(settings.DATA_DIR, exist_ok=True)
