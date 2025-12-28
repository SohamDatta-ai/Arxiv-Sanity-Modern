import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal, engine, Base
from app.services.arxiv_service import ArxivFetcher

def main():
    print("Initializing Database...")
    Base.metadata.create_all(bind=engine)
    
    print("Starting Fetch...")
    db = SessionLocal()
    fetcher = ArxivFetcher(db)
    
    # Fetch a reasonable amount for the first run
    fetcher.fetch_papers(max_results=50) # Small batch for speed
    
    print("Fetch complete.")

if __name__ == "__main__":
    main()
