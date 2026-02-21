# Errores personalizados para la autenticación del chatbot

class AuthError(Exception):
    """Clase base para errores de autenticación."""
    pass

class UserNotFoundError(AuthError):
    """Se lanza cuando el usuario no existe en la base de datos."""
    pass

class InvalidPasswordError(AuthError):
    """Se lanza cuando la contraseña es incorrecta."""
    pass

class PasswordFormatError(AuthError):
    """Se lanza cuando la contraseña no cumple con el formato requerido."""
    pass

class EmptyUsernameError(AuthError):
    """Se lanza cuando no se ingresa nombre de usuario."""
    pass

class InvalidUsernameFormatError(AuthError):
    """Se lanza cuando el usuario no cumple con el formato de correo."""
    pass

class EmptyPasswordError(AuthError):
    """Se lanza cuando no se ingresa contraseña."""
    pass

class AccountLockedError(AuthError):
    """Se lanza cuando la cuenta está bloqueada por múltiples intentos fallidos."""
    pass

class UsernameTooShortError(AuthError):
    """Se lanza cuando el nombre de usuario es demasiado corto."""
    pass

class PasswordTooShortError(AuthError):
    """Se lanza cuando la contraseña es demasiado corta."""
    pass