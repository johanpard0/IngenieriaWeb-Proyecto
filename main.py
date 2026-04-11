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
        "Puedes revisar los horarios en la plataforma académica.",
        "Los horarios de clases se publican en el portal institucional."
    ],
    "salones": [
        "Los salones están distribuidos por bloques. ¿Cuál necesitas?",
        "Puedes consultar los salones por bloque y piso.",
        "¿Qué salón deseas ubicar?"
    ],
    "profesores": [
        "Puedes consultar los profesores por materia.",
        "¿Sobre qué profesor necesitas información?",
        "Dime la materia y te indico el docente."
    ]
}

# =========================
# RUTAS HTML
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
    user_message = chat_message.message.lower()

    # SALUDOS
    if "hola" in user_message or "buenos días" in user_message or "hey" in user_message:
        response = random.choice(responses["saludos"])

    # SALONES
    elif "salon" in user_message or "salón" in user_message:
        if "a101" in user_message:
            response = "El salón A101 está en el bloque A, primer piso."
        elif "b202" in user_message:
            response = "El salón B202 está en el bloque B, segundo piso."
        else:
            response = random.choice(responses["salones"])

    # PROFESORES
    elif "profesor" in user_message or "quien dicta" in user_message:
        if "bases de datos" in user_message:
            response = "Bases de Datos la dicta el profesor Carlos Pérez en el salón A101."
        elif "redes" in user_message:
            response = "Redes la dicta la profesora Ana Gómez en el salón B202."
        else:
            response = random.choice(responses["profesores"])

    # HORARIOS
    elif "horario" in user_message:
        response = random.choice(responses["horarios"])

    # PERFIL
    elif "perfil" in user_message:
        response = "Perfil de usuario: Usuario activo. Puedes ver opciones en el menú."

    # CONFIGURACION
    elif "configuracion" in user_message or "configuración" in user_message:
        response = "Configuración: puedes cambiar contraseña, idioma y más opciones próximamente."

    # HISTORIAL
    elif "historial" in user_message:
        response = "Historial disponible próximamente."

    # FORMULARIOS
    elif "formulario" in user_message:
        response = "Usa el botón de formulario para hacer solicitudes."

    # DEFAULT
    else:
        response = "No entendí tu mensaje. Intenta con: ¿Dónde queda el salón A101?"

    return {"respuesta": response}