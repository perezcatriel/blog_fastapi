from fastapi import FastAPI, Depends
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from sqlalchemy.orm import Session


from models import Base, Blog
from schemas import BlogCreate, Blog

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/blog/", response_model=Blog)
def create_blog(blog: BlogCreate, db: Session = Depends(SessionLocal)):
    db_blog = Blog(title=blog.title, content=blog.content)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    db.close()
    return db_blog

@app.get("/blog/{blog_id}", response_model=Blog)
def read_blog(blog_id: int, db: Session = Depends(SessionLocal)):
    db_blog = db.query(Blog).filter(Blog.id == blog_id).first()
    db.close()
    return db_blog