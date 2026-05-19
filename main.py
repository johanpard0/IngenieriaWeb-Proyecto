import os

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
from backend.documento_schema import Documento

from backend.factories.app_service_factory import AppServiceFactory

load_dotenv()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Catalina API")

# =========================
# FACTORY SERVICES
# =========================

auth_service = AppServiceFactory.create_auth_service()

chat_service = AppServiceFactory.create_chat_service()

file_service = AppServiceFactory.create_file_service(
    UPLOAD_DIR
)

# =========================
# MIDDLEWARE
# =========================

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "dev-secret-key-change-this"),
)

# =========================
# STATIC FILES
# =========================

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

templates = Jinja2Templates(directory="frontend/templates")

# =========================
# ENV VARIABLES
# =========================

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

MICROSOFT_CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID")
MICROSOFT_CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET")

MICROSOFT_TENANT_ID = os.getenv(
    "MICROSOFT_TENANT_ID",
    "common"
)

# =========================
# OAUTH
# =========================

oauth = OAuth()

if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:

    oauth.register(
        name="google",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={
            "scope": "openid email profile"
        },
    )

if MICROSOFT_CLIENT_ID and MICROSOFT_CLIENT_SECRET:

    oauth.register(
        name="microsoft",
        client_id=MICROSOFT_CLIENT_ID,
        client_secret=MICROSOFT_CLIENT_SECRET,
        server_metadata_url=f"https://login.microsoftonline.com/{MICROSOFT_TENANT_ID}/v2.0/.well-known/openid-configuration",
        client_kwargs={
            "scope": "openid email profile User.Read"
        },
    )

# =========================
# DATABASE TEMP
# =========================

documentos_db = []

# =========================
# PAGES
# =========================

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):

    template = templates.get_template("login.html")

    return HTMLResponse(
        template.render(request=request)
    )


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):

    template = templates.get_template("register.html")

    return HTMLResponse(
        template.render(request=request)
    )


@app.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):

    template = templates.get_template("chat.html")

    return HTMLResponse(
        template.render(request=request)
    )


@app.get("/auth/success", response_class=HTMLResponse)
def auth_success(request: Request):

    username = request.query_params.get("username", "")

    template = templates.get_template(
        "auth_success.html"
    )

    return HTMLResponse(
        template.render(
            request=request,
            username=username
        )
    )

# =========================
# AUTH
# =========================

@app.post("/register")
def register(user: UserCreate):

    return auth_service.register_user(user)


@app.post("/login")
def login(user: UserLogin):

    return auth_service.login_user(
        user.username,
        user.password
    )

# =========================
# GOOGLE OAUTH
# =========================

@app.get("/auth/google/login")
async def google_login(request: Request):

    if "google" not in oauth:
        raise HTTPException(
            status_code=500,
            detail="Google OAuth no está configurado"
        )

    redirect_uri = f"{BASE_URL}/auth/google/callback"

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri
    )


@app.get("/auth/google/callback")
async def google_callback(request: Request):

    if "google" not in oauth:
        raise HTTPException(
            status_code=500,
            detail="Google OAuth no está configurado"
        )

    token = await oauth.google.authorize_access_token(
        request
    )

    user_info = token.get("userinfo")

    if not user_info:
        user_info = await oauth.google.userinfo(
            token=token
        )

    email = user_info.get("email")

    name = user_info.get(
        "name",
        "Usuario Google"
    )

    provider_id = user_info.get("sub")

    if not email or not provider_id:

        raise HTTPException(
            status_code=400,
            detail="No se pudo obtener la información del usuario de Google"
        )

    social_user = SocialUserCreate(
        nombre=name,
        username=email,
        provider="google",
        provider_id=provider_id
    )

    auth_service.register_or_get_social_user(
        social_user
    )

    return RedirectResponse(
        url=f"/auth/success?username={email}",
        status_code=302
    )

# =========================
# MICROSOFT OAUTH
# =========================

@app.get("/auth/microsoft/login")
async def microsoft_login(request: Request):

    if "microsoft" not in oauth:
        raise HTTPException(
            status_code=500,
            detail="Microsoft OAuth no está configurado"
        )

    redirect_uri = f"{BASE_URL}/auth/microsoft/callback"

    return await oauth.microsoft.authorize_redirect(
        request,
        redirect_uri
    )


@app.get("/auth/microsoft/callback")
async def microsoft_callback(request: Request):

    if "microsoft" not in oauth:
        raise HTTPException(
            status_code=500,
            detail="Microsoft OAuth no está configurado"
        )

    token = await oauth.microsoft.authorize_access_token(
        request
    )

    user_info = token.get("userinfo")

    if not user_info:

        resp = await oauth.microsoft.get(
            "https://graph.microsoft.com/oidc/userinfo",
            token=token
        )

        user_info = resp.json()

    email = (
        user_info.get("email")
        or user_info.get("preferred_username")
        or user_info.get("upn")
    )

    name = user_info.get(
        "name",
        "Usuario Microsoft"
    )

    provider_id = user_info.get("sub")

    if not email or not provider_id:

        raise HTTPException(
            status_code=400,
            detail="No se pudo obtener la información del usuario de Microsoft"
        )

    social_user = SocialUserCreate(
        nombre=name,
        username=email,
        provider="microsoft",
        provider_id=provider_id
    )

    auth_service.register_or_get_social_user(
        social_user
    )

    return RedirectResponse(
        url=f"/auth/success?username={email}",
        status_code=302
    )

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

            raise HTTPException(
                status_code=400,
                detail="Ya existe un documento con ese ID"
            )

    documentos_db.append(
        documento.model_dump()
    )

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

    raise HTTPException(
        status_code=404,
        detail="Documento no encontrado"
    )

# =========================
# CHAT
# =========================

class ChatMessage(BaseModel):
    message: str


@app.post("/chat/send")
async def chatbot_response(chat_message: ChatMessage):

    response = chat_service.send_message(
        chat_message.message
    )

    return {
        "respuesta": response
    }

# =========================
# FILES
# =========================

@app.get("/files")
def list_files():

    files = []

    for filename in os.listdir(UPLOAD_DIR):

        file_path = os.path.join(
            UPLOAD_DIR,
            filename
        )

        if os.path.isfile(file_path):
            files.append(filename)

    files.sort()

    return {
        "files": files
    }


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):

    return await file_service.upload(file)


@app.delete("/files/{filename}")
def delete_file(filename: str):

    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    if not os.path.exists(file_path):

        raise HTTPException(
            status_code=404,
            detail="Archivo no encontrado"
        )

    os.remove(file_path)

    return {
        "message": "Archivo eliminado correctamente"
    }