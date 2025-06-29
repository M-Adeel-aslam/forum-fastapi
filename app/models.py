from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True, index=True)
    username=Column(String, nullable=False, unique=True)
    email=Column(String, nullable=False, unique=True)
    password=Column(String, nullable=False)

    threads = relationship("Thread", back_populates="user")
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")

class Thread(Base):
    __tablename__="threads"
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String, nullable=False)
    content=Column(String, nullable=False)
    user_id=Column(Integer, ForeignKey("users.id"))
    created_at=Column(DateTime)
    updated_at=Column(DateTime)

    user = relationship("User", back_populates="threads")
    posts = relationship("Post", back_populates="thread")



class Post(Base):
    __tablename__="posts"
    id=Column(Integer, primary_key=True, index=True)
    thread_id=Column(Integer, ForeignKey("threads.id"))
    user_id=Column(Integer, ForeignKey("users.id"))
    content= Column(String, nullable=False)
    created_at=Column(DateTime)
    updated_at=Column(DateTime)
    
    thread = relationship("Thread", back_populates="posts")
    user = relationship("User", back_populates="posts")

    comments = relationship("Comment", back_populates="post")
    


class Comment(Base):
    __tablename__="comments"
    id=Column(Integer, primary_key=True, index=True)
    post_id=Column(Integer, ForeignKey("posts.id"))
    user_id=Column(Integer, ForeignKey("users.id"))
    content = Column(String, nullable=False)
    created_at=Column(DateTime)
    updated_at=Column(DateTime)

    post= relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")
    
