from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.schemas import UserCreate, UserLogin
from backend.auth import register_user, login_user

app = FastAPI(title="Catalina API")

# static
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# templates
templates = Jinja2Templates(directory="frontend/templates")


# LOGIN PAGE
@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# REGISTER PAGE
@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


# CHAT PAGE
@app.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


# REGISTER API
@app.post("/register")
def register(user: UserCreate):
    return register_user(user)


# LOGIN API
@app.post("/login")
def login(user: UserLogin):
    return login_user(user.username, user.password)