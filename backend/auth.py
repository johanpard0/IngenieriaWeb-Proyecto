from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import text

from backend.database import SessionLocal
from backend.schemas import UserCreate, SocialUserCreate


pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    if not password_hash:
        return False
    return pwd_context.verify(password, password_hash)


def normalize_user(row):
    if not row:
        return None

    user = dict(row)
    return {
        "id_estudiante": user.get("id_estudiante"),
        "nombre": user.get("nombre"),
        "cedula": user.get("cedula"),
        "username": user.get("correo"),
        "correo": user.get("correo"),
        "password": user.get("password_hash"),
        "provider": user.get("provider") or "local",
        "provider_id": user.get("provider_id") or "",
        "activo": user.get("activo"),
    }


def find_user_by_username(username: str):
    db = SessionLocal()
    try:
        row = db.execute(
            text("""
                SELECT id_estudiante, nombre, cedula, correo, password_hash,
                       provider, provider_id, activo
                FROM estudiantes
                WHERE LOWER(correo) = LOWER(:correo)
                LIMIT 1;
            """),
            {"correo": username}
        ).mappings().first()

        return normalize_user(row)

    finally:
        db.close()


def find_user_by_provider(provider: str, provider_id: str):
    db = SessionLocal()
    try:
        row = db.execute(
            text("""
                SELECT id_estudiante, nombre, cedula, correo, password_hash,
                       provider, provider_id, activo
                FROM estudiantes
                WHERE provider = :provider
                  AND provider_id = :provider_id
                LIMIT 1;
            """),
            {
                "provider": provider,
                "provider_id": provider_id
            }
        ).mappings().first()

        return normalize_user(row)

    finally:
        db.close()


def register_user(user: UserCreate):
    existing_user = find_user_by_username(user.username)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="El usuario ya existe"
        )

    db = SessionLocal()
    try:
        password_hash = hash_password(user.password)

        result = db.execute(
            text("""
                INSERT INTO estudiantes (
                    nombre,
                    cedula,
                    correo,
                    password_hash,
                    provider,
                    provider_id,
                    activo
                )
                VALUES (
                    :nombre,
                    :cedula,
                    :correo,
                    :password_hash,
                    'local',
                    '',
                    TRUE
                )
                RETURNING id_estudiante;
            """),
            {
                "nombre": user.nombre,
                "cedula": user.cedula,
                "correo": user.username,
                "password_hash": password_hash,
            }
        )

        id_estudiante = result.scalar_one()
        db.commit()

        return {
            "message": "Usuario creado correctamente",
            "id_estudiante": id_estudiante,
            "username": user.username
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al registrar usuario: {str(e)}"
        )

    finally:
        db.close()


def register_or_get_social_user(user: SocialUserCreate):
    existing_provider_user = find_user_by_provider(
        user.provider,
        user.provider_id
    )

    if existing_provider_user:
        return existing_provider_user

    existing_email_user = find_user_by_username(user.username)

    if existing_email_user:
        return existing_email_user

    db = SessionLocal()
    try:
        result = db.execute(
            text("""
                INSERT INTO estudiantes (
                    nombre,
                    cedula,
                    correo,
                    password_hash,
                    provider,
                    provider_id,
                    activo
                )
                VALUES (
                    :nombre,
                    '',
                    :correo,
                    '',
                    :provider,
                    :provider_id,
                    TRUE
                )
                RETURNING id_estudiante;
            """),
            {
                "nombre": user.nombre,
                "correo": user.username,
                "provider": user.provider,
                "provider_id": user.provider_id,
            }
        )

        id_estudiante = result.scalar_one()
        db.commit()

        return {
            "id_estudiante": id_estudiante,
            "nombre": user.nombre,
            "username": user.username,
            "correo": user.username,
            "provider": user.provider,
            "provider_id": user.provider_id,
            "activo": True,
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al registrar usuario social: {str(e)}"
        )

    finally:
        db.close()


def login_user(username: str, password: str):
    user = find_user_by_username(username)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    if user["provider"] != "local":
        raise HTTPException(
            status_code=401,
            detail="Este usuario debe iniciar sesión con Google o Microsoft"
        )

    if not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    db = SessionLocal()
    try:
        db.execute(
            text("""
                UPDATE estudiantes
                SET ultimo_acceso = CURRENT_TIMESTAMP
                WHERE id_estudiante = :id_estudiante;
            """),
            {"id_estudiante": user["id_estudiante"]}
        )
        db.commit()

    finally:
        db.close()

    return {
        "message": "Login exitoso",
        "id_estudiante": user["id_estudiante"],
        "username": user["username"],
        "nombre": user["nombre"]
    }