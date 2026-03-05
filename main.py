from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# backend
from backend import models
from backend.database import engine, SessionLocal
from backend.schemas import UserCreate, UserLogin
from backend.auth import register_user, login_user

# crear tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Catalina API")

# -----------------------
# STATIC FILES
# -----------------------
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# -----------------------
# TEMPLATES
# -----------------------
templates = Jinja2Templates(directory="frontend/templates")

# -----------------------
# DB DEPENDENCY
# -----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------
# FRONTEND LOGIN PAGE
# -----------------------
@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# -----------------------
# REGISTER
# -----------------------
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user)

# -----------------------
# LOGIN
# -----------------------
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, user.username, user.password)