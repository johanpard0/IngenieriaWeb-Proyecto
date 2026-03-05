from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: EmailStr
    password: str

class UserLogin(BaseModel):
    username: EmailStr
    password: str