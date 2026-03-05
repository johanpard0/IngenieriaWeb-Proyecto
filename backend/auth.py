from sqlalchemy.orm import Session
from backend.models import User
from backend.schemas import UserCreate
from backend.security import hash_password, verify_password

def register_user(db: Session, user: UserCreate):

    existing_user = db.query(User).filter(User.username == user.username).first()

    if existing_user:
        return {"error": "El usuario ya existe"}

    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuario registrado correctamente"}


def login_user(db: Session, username: str, password: str):

    user = db.query(User).filter(User.username == username).first()

    if not user:
        return {"error": "Usuario no encontrado"}

    if not verify_password(password, user.password):
        return {"error": "Contraseña incorrecta"}

    return {"message": "Login exitoso"}