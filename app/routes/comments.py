from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from app import models, schema
from app.auth import verify_user
from app.database import get_db

route = APIRouter(
    prefix="/comments",
    tags=['Comments']
)


@route.post("/post/{post_id}/comments", response_model=schema.CommentOut)
async def create_comment(post_id: int, comment: schema.CommentCreate, current_user: dict = Depends(verify_user), db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id,models.Post.user_id == current_user['id']).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")

    new_comment = models.Comment(
        post_id=post_id,
        user_id=current_user['id'],
        content=comment.content,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@route.get("/post/{post_id}/comments", response_model=List[schema.CommentOut])
async def all_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(models.Comment).filter(models.Comment.post_id == post_id).all()
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found.")
    return comments


@route.put("/comments/{id}", response_model=schema.CommentOut)
async def update_comment(id: int, updated_comment: schema.CommentCreate, current_user: dict = Depends(verify_user), db: Session = Depends(get_db)):
    comment = db.query(models.Comment).filter(models.Comment.id == id, models.Comment.user_id == current_user['id']).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or unauthorized.")

    comment.content = updated_comment.content
    comment.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(comment)
    return comment

@route.delete("/comments/{id}")
async def delete_comment(id: int, current_user: dict = Depends(verify_user), db: Session = Depends(get_db)):
    comment = db.query(models.Comment).filter(models.Comment.id == id, models.Comment.user_id == current_user['id']).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or unauthorized.")

    db.delete(comment)
    db.commit()
    return {"message": f"Comment with ID {id} has been deleted."}