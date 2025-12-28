from sqlalchemy.orm import Session
from app.models.paper import Paper
import numpy as np
import logging

logger = logging.getLogger(__name__)

class SearchCache:
    def __init__(self):
        self.ids = []
        self.embeddings = None
        self.loaded = False

    def load(self, db: Session):
        logger.info("Loading paper embeddings into memory...")
        try:
            papers = db.query(Paper).filter(Paper.embedding.isnot(None)).all()
            if not papers:
                logger.info("No embeddings found in DB.")
                return

            self.ids = [p.id for p in papers]
            # embedding stored as JSON list, need to be numpy
            self.embeddings = np.array([p.embedding for p in papers])
            self.loaded = True
            logger.info(f"Loaded {len(self.ids)} embeddings.")
        except Exception as e:
            logger.error(f"Error loading cache: {e}")

search_cache = SearchCache()
