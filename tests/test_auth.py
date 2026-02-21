# tests/test_auth.py
import pytest
from chatbot.auth import Auth
from chatbot.errors import (
    AuthError,
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

@pytest.fixture
def auth():
    return Auth()

# -----------------------
# Tests de errores de usuario
# -----------------------
def test_usuario_vacio(auth):
    with pytest.raises(UsuarioVacio):
        auth.login("", "1234Abc!")

def test_usuario_muy_corto(auth):
    with pytest.raises(UsuarioMuyCorto):
        auth.login("abc", "1234Abc!")

def test_usuario_no_cumple_formato(auth):
    with pytest.raises(UsuarioNoCumpleFormato):
        auth.login("usuarioMalFormato", "1234Abc!")

def test_usuario_no_encontrado(auth):
    with pytest.raises(UsuarioNoEncontrado):
        auth.login("noexiste@correo.com", "1234Abc!")

# -----------------------
# Tests de errores de contraseña
# -----------------------
def test_contrasena_vacia(auth):
    with pytest.raises(ContrasenaVacia):
        auth.login("johan@example.com", "")

def test_contrasena_muy_corta(auth):
    with pytest.raises(ContrasenaMuyCorta):
        auth.login("johan@example.com", "123")

def test_contrasena_no_cumple_formato(auth):
    with pytest.raises(ContrasenaNoCumpleFormato):
        auth.login("johan@example.com", "123456")

def test_contrasena_invalida(auth):
    with pytest.raises(ContrasenaInvalida):
        auth.login("luis@correo.com", "wrongpass")

# -----------------------
# Test de login exitoso
# -----------------------
def test_login_exitoso(auth):
    mensaje = auth.login("johan@example.com", "1234Abc!")
    assert mensaje == "Bienvenido, johan@example.com!"

# -----------------------
# Test de cuenta bloqueada por múltiples intentos
# -----------------------
def test_cuenta_bloqueada(auth):
    usuario = "luis@correo.com"
    # Forzamos 3 intentos fallidos
    for _ in range(auth.max_attempts):
        try:
            auth.login(usuario, "wrongpass")
        except ContrasenaInvalida:
            pass
    # Ahora la cuenta debe estar bloqueada
    with pytest.raises(CuentaBloqueadaIntentosFallidos):
        auth.login(usuario, "Pass123!")

# -----------------------
# Test que combina usuario y contraseña inválida
# -----------------------
def test_usuario_y_contrasena_invalidos(auth):
    with pytest.raises(UsuarioNoEncontrado):
        auth.login("desconocido@correo.com", "wrongpass")