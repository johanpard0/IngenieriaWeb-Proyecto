import csv
import os
from fastapi import HTTPException
from backend.schemas import UserCreate

FILE = "users.csv"


def read_users():
    if not os.path.exists(FILE):
        return []

    users = []

    with open(FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            users.append(row)

    return users


def save_user(nombre, cedula, username, password):

    file_exists = os.path.exists(FILE)

    with open(FILE, "a", newline="") as f:

        fieldnames = ["nombre", "cedula", "username", "password"]

        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "nombre": nombre,
            "cedula": cedula,
            "username": username,
            "password": password
        })


def register_user(user: UserCreate):

    users = read_users()

    for u in users:
        if u["username"] == user.username:
            raise HTTPException(
                status_code=400,
                detail="El usuario ya existe"
            )

    save_user(user.nombre, user.cedula, user.username, user.password)

    return {"message": "Usuario creado correctamente"}


def login_user(username: str, password: str):

    users = read_users()

    for u in users:
        if u["username"] == username and u["password"] == password:
            return {"message": "Login exitoso"}

    raise HTTPException(
        status_code=401,
        detail="Usuario o contraseña incorrectos"
    )