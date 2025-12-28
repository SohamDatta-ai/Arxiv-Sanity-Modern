import sys
import os
sys.path.append(os.getcwd())
from app.core.database import SessionLocal
from app.models.paper import Paper

db = SessionLocal()
count = db.query(Paper).count()
print(f"Paper count in DB: {count}")
