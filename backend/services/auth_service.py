from fastapi import HTTPException

class AuthService:

    def __init__(self, repository):
        self.repository = repository

    def register_user(self, user):

        existing_user = self.repository.find_by_username(
            user.username
        )

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="El usuario ya existe"
            )

        self.repository.save({
            "nombre": user.nombre,
            "cedula": user.cedula,
            "username": user.username,
            "password": user.password,
            "provider": "local",
            "provider_id": ""
        })

        return {
            "message": "Usuario creado correctamente",
            "username": user.username
        }

    def login_user(self, username: str, password: str):

        user = self.repository.find_by_username(username)

        if not user or user.get("password") != password:

            raise HTTPException(
                status_code=401,
                detail="Usuario o contraseña incorrectos"
            )

        return {
            "message": "Login exitoso",
            "username": user["username"]
        }

    def register_or_get_social_user(self, social_user):

        existing_user = self.repository.find_by_provider(
            social_user.provider,
            social_user.provider_id
        )

        if existing_user:
            return existing_user

        new_user = {
            "nombre": social_user.nombre,
            "cedula": "",
            "username": social_user.username,
            "password": "",
            "provider": social_user.provider,
            "provider_id": social_user.provider_id
        }

        self.repository.save(new_user)

        return new_user