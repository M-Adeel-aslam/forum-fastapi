from fastapi import APIRouter, Depends,HTTPException
from app import models, schema
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from app.auth import verify_user
from app.database import get_db
from datetime import datetime
from typing import List

route = APIRouter(
    prefix="/post",
    tags=['Post']
)



@route.post("/threads/{thread_id}/posts", response_model=schema.PostOut)
async def create_post(thread_id: int, user: schema.PostCreate, current_user: dict = Depends(verify_user), db: Session = Depends(get_db)):
    thread = db.query(models.Thread).filter(
        models.Thread.user_id == current_user['id'],
        models.Thread.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    newPost = models.Post(
        thread_id=thread_id,
        user_id=current_user['id'],
        content=user.content,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()  
    )
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost


@route.get("/threads/{thread_id}/posts", response_model=List[schema.PostOut])
async def view_post_of_a_thread_by_id(thread_id: int, current_user: dict = Depends(verify_user), db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.thread_id == thread_id).all()
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found for this thread.")
    return posts

@route.put("/post/{id}", response_model=schema.UpdatePostOut)
async def update_post(id: int, updatedPost: schema.UpdatePost, current_user: dict = Depends(verify_user), db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.user_id == current_user['id'], models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized.")

    post.content = updatedPost.content
    post.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(post)
    return post

@route.delete("/post/{id}")
async def delete_post(id: int, current_user: dict = Depends(verify_user), db: Session = Depends(get_db)):
    postToDelete = db.query(models.Post).filter(models.Post.user_id == current_user['id'], models.Post.id == id).first()

    if not postToDelete:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized.")

    db.delete(postToDelete)
    db.commit()
    return {"message": f"Post with ID {id} has been deleted"}


@route.get("/threads/{id}/full", response_model=schema.FullThreadOut)
async def get_full_thread(id: int, db: Session = Depends(get_db)):
    thread = db.query(models.Thread).options(
        joinedload(models.Thread.posts).joinedload(models.Post.comments)
    ).filter(models.Thread.id == id).first()

    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread