from pydantic import BaseModel, EmailStr

# Modelo para el registro de usuario
class UserCreate(BaseModel):
    nombre: str
    cedula: str
    username: str
    password: str

# Modelo para el inicio de sesión de usuario
class UserLogin(BaseModel):
    username: str  # Cambié de EmailStr a str
    password: str