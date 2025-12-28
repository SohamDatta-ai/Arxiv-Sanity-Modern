from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.user import Library
from app.models.paper import Paper

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/hype")
async def top_hype(request: Request, db: Session = Depends(get_db)):
    """
    Returns papers sorted by number of saves in user libraries.
    """
    # Count saves per paper
    # SELECT paper_id, COUNT(*) as count FROM library GROUP BY paper_id ORDER BY count DESC
    hype_query = db.query(
        Library.paper_id, 
        func.count(Library.paper_id).label('count')
    ).group_by(Library.paper_id).order_by(func.count(Library.paper_id).desc()).limit(50).all()
    
    if not hype_query:
         return templates.TemplateResponse("partials/paper_list.html", {"request": request, "papers": []})

    # Get paper objects
    top_ids = [r[0] for r in hype_query]
    papers = db.query(Paper).filter(Paper.id.in_(top_ids)).all()
    
    # Sort papers by the order in top_ids (descending count)
    papers_map = {p.id: p for p in papers}
    ordered_papers = []
    for pid in top_ids:
        if pid in papers_map:
            ordered_papers.append(papers_map[pid])

    return templates.TemplateResponse("partials/paper_list.html", {"request": request, "papers": ordered_papers})
