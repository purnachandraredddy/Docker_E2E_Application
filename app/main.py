import os
import redis
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import Base, engine, get_db
import crud, schemas, models

# Create tables via Alembic migrations in real flows; for demo we ensure metadata exists
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Docker E2E")

redis_client = redis.Redis(host=os.getenv("REDIS_HOST","redis"), port=6379, decode_responses=True)

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/users", response_model=schemas.UserOut, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_user(db, user)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not create user")

@app.get("/users", response_model=list[schemas.UserOut])
def users(db: Session = Depends(get_db)):
    return crud.list_users(db)

@app.post("/counter")
def counter():
    val = redis_client.incr("hits")
    return {"hits": val}