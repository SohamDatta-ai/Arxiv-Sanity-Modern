from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User, Library
from app.models.paper import Paper
from app.core.cache import search_cache
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/recommend")
def recommend(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Returns papers similar to the user's library.
    Logic: Average embedding of library items -> Nearest Neighbors.
    """
    # 1. Get Library Items
    lib_items = db.query(Library).filter(Library.user_id == current_user.id).all()
    if not lib_items:
        return templates.TemplateResponse("partials/paper_list.html", {"request": request, "papers": []})
    
    lib_ids = [item.paper_id for item in lib_items]

    # 2. Get Embeddings
    if not search_cache.loaded:
        search_cache.load(db)
    
    # Indices of library papers in the cache
    lib_indices = [i for i, pid in enumerate(search_cache.ids) if pid in lib_ids]
    
    if not lib_indices:
        return templates.TemplateResponse("partials/paper_list.html", {"request": request, "papers": []})

    # 3. Calculate Mean Embedding (User Vector)
    user_embedding = np.mean(search_cache.embeddings[lib_indices], axis=0)
    
    # 4. Find Similar (Cos Sim)
    sim_scores = cosine_similarity(user_embedding.reshape(1, -1), search_cache.embeddings)[0]
    
    # 5. Filter out papers already in library
    # Set score of library items to -1 so they aren't picked
    for idx in lib_indices:
        sim_scores[idx] = -1.0
        
    # 6. Top N
    top_indices = np.argsort(sim_scores)[::-1][:30]
    top_ids = [search_cache.ids[i] for i in top_indices]
    
    # 7. Fetch DB Objects
    papers = db.query(Paper).filter(Paper.id.in_(top_ids)).all()
    papers_map = {p.id: p for p in papers}
    ordered_papers = [papers_map[pid] for pid in top_ids if pid in papers_map]
    
    return templates.TemplateResponse("partials/paper_list.html", {"request": request, "papers": ordered_papers})
