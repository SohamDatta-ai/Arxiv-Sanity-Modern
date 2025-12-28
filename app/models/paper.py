from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from app.core.database import Base
from datetime import datetime

class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    arxiv_id = Column(String, unique=True, index=True)
    version = Column(Integer, default=1)
    
    title = Column(String, index=True)
    authors = Column(JSON) # List of author names
    summary = Column(Text) # Abstract
    
    published = Column(DateTime)
    updated = Column(DateTime)
    
    category = Column(String) # Primary category
    links = Column(JSON) # Stores pdf, abs links
    
    # Metadata for the "Modern" twist
    embedding = Column(JSON) # Store as list of floats (simplest approach for now)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Paper {self.arxiv_id}: {self.title}>"
