from fastapi import FastAPI, Request, Depends, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.paper import Paper
from app.services.embedding_service import get_embedder
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.routers import auth, library, recommend, hype
from fastapi.responses import RedirectResponse
from app.core.database import engine, Base
from app.core.cache import search_cache

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="A modern, clean implementation of Arxiv Sanity Preserver"
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Security & Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In strict prod, change to specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include Routers
app.include_router(auth.router)
app.include_router(library.router)
app.include_router(recommend.router)
app.include_router(hype.router)

@app.on_event("startup")
def startup_event():
    db = next(get_db())
    search_cache.load(db)

@app.get("/")
async def index(request: Request, db: Session = Depends(get_db)):
    # Recent papers
    papers = db.query(Paper).order_by(Paper.published.desc()).limit(30).all()
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "papers": papers
    })

@app.get("/search")
async def search(request: Request, q: str = "", db: Session = Depends(get_db)):
    if not q:
        # Return recent if empty query
        papers = db.query(Paper).order_by(Paper.published.desc()).limit(30).all()
        return templates.TemplateResponse("partials/paper_list.html", {"request": request, "papers": papers})

    # 1. Semantic Search
    if search_cache.loaded:
        import asyncio
        loop = asyncio.get_event_loop()

        # Define the CPU-bound operation
        def cpu_bound_search(query_text, embeddings, ids):
            embedder = get_embedder() # Lightweight singleton access
            q_emb = embedder.model.encode(query_text)
            sim_scores = cosine_similarity(q_emb.reshape(1, -1), embeddings)[0]
            top_indices = np.argsort(sim_scores)[::-1][:30]
            return [ids[i] for i in top_indices]

        # Run in threadpool so we don't block the server loop
        top_ids = await loop.run_in_executor(None, cpu_bound_search, q, search_cache.embeddings, search_cache.ids)
        
        # Fetch papers (preserve order)
        # SQL `IN` doesn't preserve order, so we fetch and sort in python
        papers = db.query(Paper).filter(Paper.id.in_(top_ids)).all()
        papers_map = {p.id: p for p in papers}
        ordered_papers = [papers_map[pid] for pid in top_ids if pid in papers_map]
        
        return templates.TemplateResponse("partials/paper_list.html", {"request": request, "papers": ordered_papers})
    
    else:
        # Fallback to simple Keyword match if no embeddings (or reload failed)
        papers = db.query(Paper).filter(Paper.title.contains(q)).limit(30).all()
        return templates.TemplateResponse("partials/paper_list.html", {"request": request, "papers": papers})

@app.get("/similar/{paper_id}")
async def similar(request: Request, paper_id: int, db: Session = Depends(get_db)):
    # 1. Find the target paper
    target_paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if not target_paper or not search_cache.loaded:
        return templates.TemplateResponse("partials/paper_list.html", {"request": request, "papers": []})
        
    # 2. Get its index in cache
    try:
        idx = search_cache.ids.index(paper_id)
    except ValueError:
        return templates.TemplateResponse("partials/paper_list.html", {"request": request, "papers": []})

    # 3. Compute similarity
    target_emb = search_cache.embeddings[idx]
    sim_scores = cosine_similarity(target_emb.reshape(1, -1), search_cache.embeddings)[0]
    
    # 4. Top N (exclude self)
    top_indices = np.argsort(sim_scores)[::-1][1:31] # Skip index 0 (self)
    
    top_ids = [search_cache.ids[i] for i in top_indices]
    
    papers = db.query(Paper).filter(Paper.id.in_(top_ids)).all()
    papers_map = {p.id: p for p in papers}
    ordered_papers = [papers_map[pid] for pid in top_ids if pid in papers_map]
    
    return templates.TemplateResponse("partials/paper_list.html", {"request": request, "papers": ordered_papers})

@app.post("/reload")
async def reload_cache(db: Session = Depends(get_db)):
    """Reloads the in-memory embedding cache."""
    search_cache.load(db)
    return {"message": "Cache reloaded", "count": len(search_cache.ids)}

@app.get("/login-page")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register-page")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
