from fastapi import FastAPI, Request, HTTPException, Query, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.schemas import UserCreate
from backend.auth import register_user, login_user
from backend.documento_schema import Documento

app = FastAPI(title="Catalina API")

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

documentos_db = []


# =========================
# RUTAS DEL PROYECTO ACTUAL
# =========================

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {})


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request, "register.html", {})


@app.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    return templates.TemplateResponse(request, "chat.html", {})


@app.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...)
):
    user = UserCreate(username=username, password=password)
    register_user(user)
    return RedirectResponse(url="/", status_code=303)


@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...)
):
    login_user(username, password)
    return RedirectResponse(url="/chat", status_code=303)


# =========================
# RUTAS NUEVAS DEL TALLER
# =========================

@app.get("/documentos")
def obtener_documentos():
    return documentos_db


@app.post("/documentos")
def crear_documento(documento: Documento):
    for doc in documentos_db:
        if doc["id"] == documento.id:
            raise HTTPException(status_code=400, detail="Ya existe un documento con ese ID")

    documentos_db.append(documento.model_dump())
    return {
        "mensaje": "Documento creado correctamente",
        "documento": documento
    }


@app.get("/documentos/filtro/buscar")
def filtrar_documentos(
    categoria: str | None = Query(default=None, description="Filtrar por categoría"),
    activo: bool | None = Query(default=None, description="Filtrar por estado activo/inactivo")
):
    resultados = documentos_db

    if categoria is not None:
        resultados = [
            doc for doc in resultados
            if doc["categoria"].lower() == categoria.lower()
        ]

    if activo is not None:
        resultados = [
            doc for doc in resultados
            if doc["activo"] == activo
        ]

    return resultados


@app.get("/documentos/{id}")
def obtener_documento_por_id(id: int):
    for doc in documentos_db:
        if doc["id"] == id:
            return doc

    raise HTTPException(status_code=404, detail="Documento no encontrado")