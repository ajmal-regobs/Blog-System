from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.models import Blog
from app.schemas import BlogCreate, BlogResponse

router = APIRouter()


@router.get("/health")
def health_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception:
        raise HTTPException(
            status_code=503,
            detail={"status": "unhealthy", "database": "disconnected"},
        )


@router.post("/blogs", response_model=BlogResponse, status_code=201)
def add_blog(blog: BlogCreate, db: Session = Depends(get_db)):
    db_blog = Blog(title=blog.title, content=blog.content, author=blog.author)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog


@router.get("/blogs", response_model=list[BlogResponse])
def list_blogs(db: Session = Depends(get_db)):
    return db.query(Blog).order_by(Blog.created_at.desc()).all()


@router.delete("/blogs/{blog_id}", status_code=204)
def remove_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    db.delete(blog)
    db.commit()
