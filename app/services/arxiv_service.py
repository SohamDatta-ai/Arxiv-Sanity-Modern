import urllib.request
import urllib.parse
import feedparser
import time
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.paper import Paper
from app.core.database import SessionLocal
import dateutil.parser
# Import embedder
from app.services.embedding_service import get_embedder

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ArxivFetcher:
    BASE_URL = 'https://export.arxiv.org/api/query?'

    def __init__(self, db: Session):
        self.db = db
        try:
            self.embedder = get_embedder()
        except Exception as e:
            logger.warning(f"Warning: Could not load embedder. Semantic search will be disabled. Error: {e}")
            self.embedder = None

    def fetch_papers(self, search_query="cat:cs.CV OR cat:cs.AI OR cat:cs.LG", max_results=200):
        logger.info(f"Fetching {max_results} papers for query: {search_query}")
        
        # Build query
        query_params = {
            "search_query": search_query,
            "start": 0,
            "max_results": max_results,
            "sortBy": "lastUpdatedDate",
            "sortOrder": "descending"
        }
        
        # Ensure we don't have spaces in URL (though requests handles it, good practice)
        # Using build_opener to avoid some bot detection
        url = f"http://export.arxiv.org/api/query?{urllib.parse.urlencode(query_params)}"
        logger.info(f"URL: {url}")
        
        op = urllib.request.build_opener()
        op.addheaders = [('User-agent', 'Mozilla/5.0')]
        
        new_papers = 0
        try:
            with op.open(url) as response:
                data = response.read()
                logger.info(f"Response size: {len(data)} bytes")
                
                feed = feedparser.parse(data)
                logger.info(f"Feed entries found: {len(feed.entries)}")
                
                if feed.bozo:
                     logger.warning(f"Feed bozo (error): {feed.bozo_exception}")

                # The original code used self.db, but the provided snippet uses self.SessionLocal()
                # Assuming SessionLocal is meant to be used here to manage sessions per fetch.
                # If self.SessionLocal is not defined, this will cause an error.
                # For now, I'll assume SessionLocal is accessible and meant to be called.
                # If the intent was to use the existing self.db, the snippet is misleading.
                # Sticking to the provided snippet's structure.
                with SessionLocal() as db:
                    for entry in feed.entries:
                        paper_data = self._parse_entry(entry)
                        # Pass DB explicitly to _save_paper
                        added = self._save_paper(db, paper_data)
                        if added:
                            new_papers += 1
                    
                    db.commit()
                    
        except Exception as e:
            logger.error(f"Error fetching from Arxiv: {e}")
            
        logger.info(f"Done. Added {new_papers} new papers.")

    def _parse_entry(self, entry):
        # Extract ID (remove version)
        id_url = entry.id
        arxiv_id = id_url.split('/abs/')[-1]
        version = 1
        if 'v' in arxiv_id:
            parts = arxiv_id.split('v')
            arxiv_id = parts[0]
            version = int(parts[1])

        # Authors
        authors = [a.name for a in entry.authors]
        
        # Links
        links = {}
        for link in entry.links:
            if link.rel == 'alternate':
                links['abs'] = link.href
            elif link.title == 'pdf':
                links['pdf'] = link.href

        return {
            "arxiv_id": arxiv_id,
            "version": version,
            "title": " ".join(entry.title.split()), # Clean newlines
            "summary": " ".join(entry.summary.split()),
            "authors": authors,
            "published": dateutil.parser.parse(entry.published),
            "updated": dateutil.parser.parse(entry.updated),
            "category": entry.arxiv_primary_category['term'],
            "links": links
        }

    def _save_paper(self, db, data):
        # Generate embedding if new or updated
        if self.embedder:
            try:
                # We do this before saving. It might be slow.
                # In production, this should be a background task (APScheduler).
                # For simplicity here (per "Code Cleanliness"), we do it synchronous.
                embedding = self.embedder.embed_paper(data['title'], data['summary'])
                data['embedding'] = embedding
            except Exception as e:
                logger.error(f"Failed to embed paper {data['arxiv_id']}: {e}")

        # Check if exists
        existing = db.query(Paper).filter(Paper.arxiv_id == data['arxiv_id']).first()
        
        if existing:
            # Update if newer version
            if data['version'] > existing.version:
                logger.info(f"Updating {data['arxiv_id']} v{existing.version} -> v{data['version']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                return True # Count as "action taken"
            return False # Skipped
        
        # Create new
        paper = Paper(**data)
        db.add(paper)
        return True

if __name__ == "__main__":
    # Test run
    db = SessionLocal()
    fetcher = ArxivFetcher(db)
    fetcher.fetch_papers(max_results=10)
