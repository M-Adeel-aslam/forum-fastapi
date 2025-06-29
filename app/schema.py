from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from typing import List


class Usercreate(BaseModel):
    username:str
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    username:str
    email:EmailStr

    class Config():
        orm_mode=True

class Loginschema(BaseModel):
    username:str
    password:str

# Threads
class ThreadCreate(BaseModel):
    title:str
    content:str

class ThreadOut(ThreadCreate):
    id:int
    user_id:int
    created_at:datetime
    updated_at:datetime

    class Config():
        orm_mode=True


# updatethread
class UpdateThread(BaseModel):
    title:str
    content:str

class UpdateThreadOut(ThreadCreate):
    id:int
    user_id:int
    created_at:datetime
    updated_at:datetime

    class Config():
        orm_mode=True


# Posts
class PostCreate(BaseModel):
    content:str

class PostOut(PostCreate):
    id:int
    thread_id:int
    user_id:int
    created_at:datetime
    updated_at:Optional[datetime]

    class Config():
        orm_mode=True

# updated post
class UpdatePost(BaseModel):
    content:str

class UpdatePostOut(UpdatePost):
    id:int
    thread_id:int
    user_id:int
    updated_at:datetime

    class Config():
        orm_mode=True

# Comment
class CommentCreate(BaseModel):
    content:str

class CommentOut(CommentCreate):
    id:int
    post_id:int
    user_id:int
    created_at:datetime
    updated_at:datetime

    class Config():
        orm_mode=True

# update comment
class CommentCreate(BaseModel):
    content: str

class CommentOut(CommentCreate):
    id: int
    post_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]  
    class Config:
        orm_mode = True

class CommentNested(BaseModel):
    id: int
    content: str
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class PostNested(BaseModel):
    id: int
    content: str
    user_id: int
    created_at: datetime
    updated_at: datetime
    comments: List[CommentNested] = []  

    class Config:
        orm_mode = True

class FullThreadOut(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    created_at: datetime
    updated_at: datetime
    posts: List[PostNested] = []  

    class Config:
        orm_mode = True