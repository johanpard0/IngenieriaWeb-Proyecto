import os
import random
import shutil

from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth

from backend.schemas import UserCreate, UserLogin, SocialUserCreate
from backend.auth import register_user, login_user, register_or_get_social_user
from backend.documento_schema import Documento

load_dotenv()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Catalina API")

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "dev-secret-key-change-this"),
)

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
MICROSOFT_CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID")
MICROSOFT_CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET")
MICROSOFT_TENANT_ID = os.getenv("MICROSOFT_TENANT_ID", "common")

oauth = OAuth()

if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
    oauth.register(
        name="google",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

if MICROSOFT_CLIENT_ID and MICROSOFT_CLIENT_SECRET:
    oauth.register(
        name="microsoft",
        client_id=MICROSOFT_CLIENT_ID,
        client_secret=MICROSOFT_CLIENT_SECRET,
        server_metadata_url=f"https://login.microsoftonline.com/{MICROSOFT_TENANT_ID}/v2.0/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile User.Read"},
    )

documentos_db = []

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


@app.get("/auth/success", response_class=HTMLResponse)
def auth_success(request: Request):
    username = request.query_params.get("username", "")
    template = templates.get_template("auth_success.html")
    return HTMLResponse(template.render(request=request, username=username))


@app.post("/register")
def register(user: UserCreate):
    return register_user(user)


@app.post("/login")
def login(user: UserLogin):
    return login_user(user.username, user.password)


@app.get("/auth/google/login")
async def google_login(request: Request):
    if "google" not in oauth:
        raise HTTPException(status_code=500, detail="Google OAuth no está configurado")

    redirect_uri = f"{BASE_URL}/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get("/auth/google/callback")
async def google_callback(request: Request):
    if "google" not in oauth:
        raise HTTPException(status_code=500, detail="Google OAuth no está configurado")

    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")

    if not user_info:
        user_info = await oauth.google.userinfo(token=token)

    email = user_info.get("email")
    name = user_info.get("name", "Usuario Google")
    provider_id = user_info.get("sub")

    if not email or not provider_id:
        raise HTTPException(status_code=400, detail="No se pudo obtener la información del usuario de Google")

    social_user = SocialUserCreate(
        nombre=name,
        username=email,
        provider="google",
        provider_id=provider_id
    )
    register_or_get_social_user(social_user)

    return RedirectResponse(url=f"/auth/success?username={email}", status_code=302)


@app.get("/auth/microsoft/login")
async def microsoft_login(request: Request):
    if "microsoft" not in oauth:
        raise HTTPException(status_code=500, detail="Microsoft OAuth no está configurado")

    redirect_uri = f"{BASE_URL}/auth/microsoft/callback"
    return await oauth.microsoft.authorize_redirect(request, redirect_uri)


@app.get("/auth/microsoft/callback")
async def microsoft_callback(request: Request):
    if "microsoft" not in oauth:
        raise HTTPException(status_code=500, detail="Microsoft OAuth no está configurado")

    token = await oauth.microsoft.authorize_access_token(request)
    user_info = token.get("userinfo")

    if not user_info:
        resp = await oauth.microsoft.get("https://graph.microsoft.com/oidc/userinfo", token=token)
        user_info = resp.json()

    email = (
        user_info.get("email")
        or user_info.get("preferred_username")
        or user_info.get("upn")
    )
    name = user_info.get("name", "Usuario Microsoft")
    provider_id = user_info.get("sub")

    if not email or not provider_id:
        raise HTTPException(status_code=400, detail="No se pudo obtener la información del usuario de Microsoft")

    social_user = SocialUserCreate(
        nombre=name,
        username=email,
        provider="microsoft",
        provider_id=provider_id
    )
    register_or_get_social_user(social_user)

    return RedirectResponse(url=f"/auth/success?username={email}", status_code=302)


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


class ChatMessage(BaseModel):
    message: str


@app.post("/chat/send")
async def chatbot_response(chat_message: ChatMessage):
    user_message = chat_message.message.lower()

    if "hola" in user_message or "buenos días" in user_message or "hey" in user_message:
        response = random.choice(responses["saludos"])
    elif "salon" in user_message or "salón" in user_message:
        if "a101" in user_message:
            response = "El salón A101 está en el bloque A, primer piso."
        elif "b202" in user_message:
            response = "El salón B202 está en el bloque B, segundo piso."
        else:
            response = random.choice(responses["salones"])
    elif "profesor" in user_message or "quien dicta" in user_message:
        if "bases de datos" in user_message:
            response = "Bases de Datos la dicta el profesor Carlos Pérez en el salón A101."
        elif "redes" in user_message:
            response = "Redes la dicta la profesora Ana Gómez en el salón B202."
        else:
            response = random.choice(responses["profesores"])
    elif "horario" in user_message:
        response = random.choice(responses["horarios"])
    elif "perfil" in user_message:
        response = "Perfil de usuario: Usuario activo. Puedes ver opciones en el menú."
    elif "configuracion" in user_message or "configuración" in user_message:
        response = "Configuración: puedes cambiar contraseña, idioma y más opciones próximamente."
    elif "historial" in user_message:
        response = "Historial disponible próximamente."
    elif "formulario" in user_message:
        response = "Usa el botón de formulario para hacer solicitudes."
    else:
        response = "No entendí tu mensaje. Intenta con: ¿Dónde queda el salón A101?"

    return {"respuesta": response}

@app.get("/files")
def list_files():
    files = []

    for filename in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.isfile(file_path):
            files.append(filename)

    files.sort()
    return {"files": files}


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "Archivo subido correctamente", "filename": file.filename}


@app.delete("/files/{filename}")
def delete_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    os.remove(file_path)
    return {"message": "Archivo eliminado correctamente"}