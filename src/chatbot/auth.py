import re
from .errors import (
    ErrorAunteticacion,
    UsuarioNoEncontrado,
    ContrasenaInvalida,
    ContrasenaNoCumpleFormato,
    UsuarioVacio,
    UsuarioNoCumpleFormato,
    ContrasenaVacia,
    CuentaBloqueadaIntentosFallidos,
    UsuarioMuyCorto,
    ContrasenaMuyCorta
)

class Auth:
    """Clase de autenticación para el chatbot."""

    def __init__(self):
        # Base de datos simulada: usuario -> contraseña
        self.users_db = {
            "johan@example.com": "1234Abc!",
            "ana@test.com": "Ana12345",
            "luis@correo.com": "Pass123!"
        }
        # Control de intentos fallidos
        self.failed_attempts = {}
        # Límite de intentos antes de bloquear la cuenta
        self.max_attempts = 3

    # -----------------------
    # Validaciones
    # -----------------------
    def validar_usuario(self, username: str):
        if not username:
            raise UsuarioVacio("El usuario no puede estar vacío.")
        if len(username) < 5:
            raise UsuarioMuyCorto("El usuario es demasiado corto.")
        # Validación de formato de email
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, username):
            raise UsuarioNoCumpleFormato("El usuario debe ser un email válido.")

    def validar_contrasena(self, password: str):
        if not password:
            raise ContrasenaVacia("La contraseña no puede estar vacía.")
        if len(password) < 6:
            raise ContrasenaMuyCorta("La contraseña es demasiado corta.")
        # Validación básica: debe tener letra y número
        if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
            raise ContrasenaNoCumpleFormato("La contraseña debe contener letras y números.")

    # -----------------------
    # Login
    # -----------------------
    def login(self, username: str, password: str) -> str:
        """Intenta iniciar sesión y devuelve un mensaje de éxito o lanza errores."""

        # Validar usuario y contraseña
        self.validar_usuario(username)
        self.validar_contrasena(password)

        # Verificar si la cuenta está bloqueada por intentos fallidos
        if self.failed_attempts.get(username, 0) >= self.max_attempts:
            raise CuentaBloqueadaIntentosFallidos(f"La cuenta '{username}' está bloqueada por múltiples intentos fallidos.")

        # Verificar usuario
        if username not in self.users_db:
            self.failed_attempts[username] = self.failed_attempts.get(username, 0) + 1
            raise UsuarioNoEncontrado(f"Usuario '{username}' no encontrado.")

        # Verificar contraseña
        if self.users_db[username] != password:
            self.failed_attempts[username] = self.failed_attempts.get(username, 0) + 1
            raise ContrasenaInvalida("Contraseña incorrecta.")

        # Login exitoso: resetear intentos
        self.failed_attempts[username] = 0
        return f"Bienvenido, {username}!"