from sentence_transformers import SentenceTransformer
import numpy as np

import logging
logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        # This will download the model on first use (~80MB)
        logger.info(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        logger.info("Model loaded.")

    def embed_paper(self, title: str, summary: str) -> list[float]:
        """
        Creates a text embedding for the paper.
        Combines title and summary for the semantic representation.
        """
        # Prefixing title might give it slightly more weight or context
        text = f"{title}. {summary}"
        
        # Encode
        embedding = self.model.encode(text)
        
        # Convert to list for JSON serialization (if using generic JSON storage)
        return embedding.tolist()

# Singleton instance to avoid reloading model
_embedder_instance = None

def get_embedder():
    global _embedder_instance
    if _embedder_instance is None:
        _embedder_instance = EmbeddingService()
    return _embedder_instance
