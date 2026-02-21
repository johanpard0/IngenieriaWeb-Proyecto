# Errores personalizados para la autenticación del chatbot

class AuthError(Exception):
    """Clase base para errores de autenticación."""
    pass

class UsuarioNoEncontrado(AuthError):
    """Se lanza cuando el usuario no existe en la base de datos."""
    pass

class ContrasenaInvalida(AuthError):
    """Se lanza cuando la contraseña es incorrecta."""
    pass

class ContrasenaNoCumpleFormato(AuthError):
    """Se lanza cuando la contraseña no cumple con el formato requerido."""
    pass

class UsuarioVacio(AuthError):
    """Se lanza cuando no se ingresa nombre de usuario."""
    pass

class UsuarioNoCumpleFormato(AuthError):
    """Se lanza cuando el usuario no cumple con el formato de correo."""
    pass

class ContrasenaVacia(AuthError):
    """Se lanza cuando no se ingresa contraseña."""
    pass

class CuentaBloqueadaIntentosFallidos(AuthError):
    """Se lanza cuando la cuenta está bloqueada por múltiples intentos fallidos."""
    pass

class UsuarioMuyCorto(AuthError):
    """Se lanza cuando el nombre de usuario es demasiado corto."""
    pass

class ContrasenaMuyCorta(AuthError):
    """Se lanza cuando la contraseña es demasiado corta."""
    pass