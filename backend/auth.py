import csv
import os
from fastapi import HTTPException
from backend.schemas import UserCreate, SocialUserCreate

FILE = "users.csv"
FIELDNAMES = ["nombre", "cedula", "username", "password", "provider", "provider_id"]


def read_users():
    if not os.path.exists(FILE):
        return []

    users = []

    with open(FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            normalized = {
                "nombre": row.get("nombre", ""),
                "cedula": row.get("cedula", ""),
                "username": row.get("username", ""),
                "password": row.get("password", ""),
                "provider": row.get("provider", "local") or "local",
                "provider_id": row.get("provider_id", ""),
            }
            users.append(normalized)

    return users


def rewrite_users(users):
    with open(FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for user in users:
            writer.writerow({
                "nombre": user.get("nombre", ""),
                "cedula": user.get("cedula", ""),
                "username": user.get("username", ""),
                "password": user.get("password", ""),
                "provider": user.get("provider", "local"),
                "provider_id": user.get("provider_id", ""),
            })


def ensure_storage():
    users = read_users()
    rewrite_users(users)


def save_user(nombre, cedula, username, password, provider="local", provider_id=""):
    ensure_storage()

    with open(FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow({
            "nombre": nombre,
            "cedula": cedula,
            "username": username,
            "password": password,
            "provider": provider,
            "provider_id": provider_id,
        })


def find_user_by_username(username: str):
    users = read_users()
    for user in users:
        if user["username"].lower() == username.lower():
            return user
    return None


def find_user_by_provider(provider: str, provider_id: str):
    users = read_users()
    for user in users:
        if user["provider"] == provider and user["provider_id"] == provider_id:
            return user
    return None


def register_user(user: UserCreate):
    existing_user = find_user_by_username(user.username)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="El usuario ya existe"
        )

    save_user(
        nombre=user.nombre,
        cedula=user.cedula,
        username=user.username,
        password=user.password,
        provider="local",
        provider_id=""
    )

    return {
        "message": "Usuario creado correctamente",
        "username": user.username
    }


def register_or_get_social_user(user: SocialUserCreate):
    existing_provider_user = find_user_by_provider(user.provider, user.provider_id)
    if existing_provider_user:
        return existing_provider_user

    existing_email_user = find_user_by_username(user.username)
    if existing_email_user:
        return existing_email_user

    save_user(
        nombre=user.nombre,
        cedula="",
        username=user.username,
        password="",
        provider=user.provider,
        provider_id=user.provider_id
    )

    return find_user_by_username(user.username)


def login_user(username: str, password: str):
    users = read_users()

    for u in users:
        if u["username"].lower() == username.lower():
            if u["provider"] != "local":
                raise HTTPException(
                    status_code=401,
                    detail="Este usuario debe iniciar sesión con Google o Microsoft"
                )

            if u["password"] == password:
                return {
                    "message": "Login exitoso",
                    "username": u["username"]
                }

    raise HTTPException(
        status_code=401,
        detail="Usuario o contraseña incorrectos"
    )