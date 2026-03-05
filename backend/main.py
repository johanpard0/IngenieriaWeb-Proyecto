from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from schemas import UserCreate, UserLogin
from auth import register_user, login_user

# Crear tablas automáticamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Catalina API")

# Dependencia de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"mensaje": "Catalina Backend funcionando 🚀"}

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user)

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, user.username, user.password)