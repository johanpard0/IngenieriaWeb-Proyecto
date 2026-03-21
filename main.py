from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.schemas import UserCreate, UserLogin
from backend.auth import register_user, login_user
from backend.documento_schema import Documento

app = FastAPI(title="Catalina API")

# static
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# templates
templates = Jinja2Templates(directory="frontend/templates")

# "Base de datos" temporal en memoria
documentos_db = []


# =========================
# RUTAS DEL PROYECTO ACTUAL
# =========================

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
def register(user: UserCreate):
    return register_user(user)


@app.post("/login")
def login(user: UserLogin):
    return login_user(user.username, user.password)


# =========================
# RUTAS NUEVAS DEL TALLER
# =========================

# 1. Endpoint lectura total (GET)
@app.get("/documentos")
def obtener_documentos():
    return documentos_db


# 2. Endpoint creación (POST)
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


# 5. Filtrado dinámico (Query Parameter)
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


# 3. Endpoint búsqueda específica (Path Parameter)
# 4. Lógica de Error con HTTPException 404
@app.get("/documentos/{id}")
def obtener_documento_por_id(id: int):
    for doc in documentos_db:
        if doc["id"] == id:
            return doc

    raise HTTPException(status_code=404, detail="Documento no encontrado")