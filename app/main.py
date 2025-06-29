from routes import authentication, threads, post, comments
from fastapi import FastAPI
from database import create_all_tables

create_all_tables()
app = FastAPI()

app.include_router(authentication.route)
app.include_router(threads.route)
app.include_router(post.route)
app.include_router(comments.route)