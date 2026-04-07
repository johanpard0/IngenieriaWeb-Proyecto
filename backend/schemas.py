from pydantic import BaseModel, EmailStr
from pydantic import BaseModel

class UserCreate(BaseModel):
    nombre: str
    cedula: str
    username: str
    password: str


class UserLogin(BaseModel):
    username: EmailStr
    password: str