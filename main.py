from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend import models
from backend.database import engine, SessionLocal
from backend.schemas import UserCreate, UserLogin
from backend.auth import register_user, login_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Catalina API")

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user)

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, user.username, user.password)

@app.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})