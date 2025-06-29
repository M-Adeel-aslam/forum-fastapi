from fastapi import APIRouter, Depends,HTTPException
import models, schema
from sqlalchemy.orm import Session
from auth import verify_user
from typing import List
from datetime import datetime
from database import get_db

route = APIRouter(
    prefix="/threads",
    tags=['Threads']
)


@route.post("/", response_model=schema.ThreadOut)
async def create_threads(user:schema.ThreadCreate, db:Session=Depends(get_db),current_user: dict = Depends(verify_user)):
    existing = db.query(models.Thread).filter(models.Thread.title == user.title).first()
    if existing:
        raise HTTPException(status_code=400, detail="Thread already exists.")
    
    newthread = models.Thread(
         user_id=current_user["id"],
         title = user.title,
         content=user.content,
         created_at= datetime.utcnow(),
         updated_at=datetime.utcnow()
    )
    db.add(newthread)
    db.commit()
    db.refresh(newthread)
    return newthread

@route.get("/", response_model=List[schema.ThreadOut])
async def all_threads(current_user: dict = Depends(verify_user), db: Session = Depends(get_db)):
    current_user_threads = db.query(models.Thread).filter(models.Thread.user_id == current_user['id']).all()
    if not current_user_threads:
        raise HTTPException(status_code=404, detail="No user thread found")
    return current_user_threads

@route.get("/{id}", response_model=schema.ThreadOut)
async def get_threads_by_id(id:int, current_user:dict=Depends(verify_user), db:Session=Depends(get_db)):
    found_threads = db.query(models.Thread).filter(models.Thread.user_id==current_user['id'],
                                                   models.Thread.id==id).first()
    if not found_threads:
        raise HTTPException(status_code=404, detail="No thread found.")
   
    return found_threads


@route.put("/{id}", response_model=schema.UpdateThreadOut)
async def update_threads(id:int,updatedThread:schema.UpdateThread, current_user:dict=Depends(verify_user), db:Session=Depends(get_db)):
    user = db.query(models.Thread).filter(models.Thread.user_id==current_user['id'],models.Thread.id==id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Thread not found or unauthorized.")

    user.title = updatedThread.title
    user.content = updatedThread.content
    user.updated_at= datetime.utcnow()    
    db.commit()
    db.refresh(user)
    return user


@route.delete("/{id}")
async def delete_threads(id:int,current_user:dict=Depends(verify_user), db:Session=Depends(get_db)):
    threadToDelete = db.query(models.Thread).filter(models.Thread.user_id==current_user['id'],models.Thread.id==id).first()
    db.delete(threadToDelete)
    db.commit()
    return {"message": f"Thread with ID {id} has been deleted"}