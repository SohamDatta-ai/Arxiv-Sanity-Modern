from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User, Library
from app.models.paper import Paper
from typing import List

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/library")
async def view_library(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """ Returns the papers in the user's library """
    # Get all paper IDs
    lib_entries = db.query(Library).filter(Library.user_id == current_user.id).all()
    paper_ids = [entry.paper_id for entry in lib_entries]
    
    # Fetch papers
    if not paper_ids:
        return templates.TemplateResponse("partials/paper_list.html", {"request": request, "papers": []})
        
    papers = db.query(Paper).filter(Paper.id.in_(paper_ids)).all()
    return templates.TemplateResponse("partials/paper_list.html", {"request": request, "papers": papers})

@router.post("/library/toggle/{paper_id}")
def toggle_library(paper_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Toggles a paper in the user's library. 
    Returns: 'ON' if added, 'OFF' if removed.
    """
    existing = db.query(Library).filter(
        Library.user_id == current_user.id, 
        Library.paper_id == paper_id
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        return "OFF"
    else:
        # Check if paper exists first
        paper = db.query(Paper).filter(Paper.id == paper_id).first()
        if not paper:
            raise HTTPException(status_code=404, detail="Paper not found")
            
        entry = Library(user_id=current_user.id, paper_id=paper_id)
        db.add(entry)
        db.commit()
        return "ON"

@router.get("/library/ids")
def get_library_ids(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """ Returns list of paper IDs in user's library """
    items = db.query(Library).filter(Library.user_id == current_user.id).all()
    return [item.paper_id for item in items]
