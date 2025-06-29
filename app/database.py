from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(url=DATABASE_URL, future=True)

local_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def create_all_tables():
    return Base.metadata.create_all(bind=engine)

def get_db():
    db=local_session()
    try:
        yield db
    finally:
        db.close()
