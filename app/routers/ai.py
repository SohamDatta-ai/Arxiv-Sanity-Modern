from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.paper import Paper
from app.services.gemini_service import get_gemini_service

router = APIRouter()

@router.get("/ai/explain/{paper_id}")
async def explain_paper(paper_id: int, db: Session = Depends(get_db)):
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if not paper:
        return "<p>Paper not found</p>"
    
    service = get_gemini_service()
    explanation = await service.explain_paper(paper.title, paper.summary)
    
    return f"""
    <div style="background: #f0fdf4; border: 1px solid #bbf7d0; padding: 15px; margin-top: 10px; border-radius: 4px; font-size: 14px; color: #166534;">
        <h4 style="margin: 0 0 5px 0; font-weight: bold;">🤖 AI Explanation</h4>
        {explanation}
    </div>
    """
