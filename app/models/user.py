from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    library_items = relationship("Library", back_populates="user")

class Library(Base):
    __tablename__ = "library"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    paper_id = Column(Integer, ForeignKey("papers.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="library_items")
    paper = relationship("Paper")
