from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.schemas import UserCreate, UserLogin
from backend.auth import register_user, login_user
from backend.documento_schema import Documento

app = FastAPI(title="Catalina API")

# Archivos estáticos
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Templates
templates = Jinja2Templates(directory="frontend/templates")

# Base de datos temporal
documentos_db = []


# =========================
# RUTAS HTML (VERSIÓN SEGURA)
# =========================

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    template = templates.get_template("login.html")
    return HTMLResponse(template.render(request=request))


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    template = templates.get_template("register.html")
    return HTMLResponse(template.render(request=request))


@app.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    template = templates.get_template("chat.html")
    return HTMLResponse(template.render(request=request))


# =========================
# AUTH
# =========================

@app.post("/register")
def register(user: UserCreate):
    return register_user(user)


@app.post("/login")
def login(user: UserLogin):
    return login_user(user.username, user.password)


# =========================
# DOCUMENTOS
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
    categoria: str | None = Query(default=None),
    activo: bool | None = Query(default=None)
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