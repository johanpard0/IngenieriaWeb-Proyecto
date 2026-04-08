from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import random

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

# Respuestas predefinidas del chatbot
responses = {
    "saludos": [
        "¡Hola! ¿En qué puedo ayudarte?",
        "¡Hola! Soy Catalina, tu asistente virtual.",
        "¡Hola! ¿Cómo puedo asistirte hoy?"
    ],
    "horarios": [
        "Los horarios de los salones están disponibles en el portal de la universidad.",
        "Puedes revisar los horarios de los salones en la plataforma de la universidad.",
        "Los horarios de clases se publican en el portal de la universidad."
    ],
    "salones": [
        "Los salones se encuentran en varios edificios de la universidad. ¿Te gustaría saber más sobre alguno?",
        "Puedes ver los detalles de los salones en el portal web de la universidad.",
        "¿Te gustaría saber sobre los salones disponibles?"
    ],
    "profesores": [
        "Los profesores están disponibles a través del portal. ¿Quieres saber sobre alguno en particular?",
        "Puedes consultar la información de los profesores en el portal de la universidad.",
        "¿Hay algún profesor sobre el que quieras saber más?"
    ]
}

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


# =========================
# CHATBOT
# =========================

class ChatMessage(BaseModel):
    message: str

@app.post("/chat/send")
async def chatbot_response(chat_message: ChatMessage):
    user_message = chat_message.message.lower()  # Convertir a minúsculas para comparar sin distinción de mayúsculas

    # Responder en función de las palabras clave en el mensaje
    if "hola" in user_message or "buenos días" in user_message or "hey" in user_message:
        response = random.choice(responses["saludos"])
    elif "horario" in user_message or "clases" in user_message:
        response = random.choice(responses["horarios"])
    elif "salon" in user_message:
        response = random.choice(responses["salones"])
    elif "profesor" in user_message:
        response = random.choice(responses["profesores"])
    else:
        response = "Lo siento, no entendí tu mensaje. ¿En qué más puedo ayudarte?"

    return {"respuesta": response}