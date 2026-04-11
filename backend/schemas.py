from pydantic import BaseModel


class UserCreate(BaseModel):
    nombre: str
    cedula: str
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class SocialUserCreate(BaseModel):
    nombre: str
    username: str
    provider: str
    provider_id: str