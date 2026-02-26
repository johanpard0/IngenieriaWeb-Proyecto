# main.py - archivo de prueba para login del chatbot

# Import absoluto desde el paquete 'chatbot'
from fastapi import FastAPI
from chatbot.auth import Auth
from chatbot.errors import AuthError

app = FastAPI()
@app.get("/")
def home()
        return {"mensaje": "Mi API esta funcioando"}

def probar_login():
    auth = Auth()

    casos_prueba = [
        {"username": "johan@example.com", "password": "1234Abc!"},
        {"username": "", "password": "1234"},
        {"username": "ana@test.com", "password": ""},
        {"username": "noexiste@correo.com", "password": "1234"},
        {"username": "luis@correo.com", "password": "wrongpass"},
        {"username": "usuarioMalFormato", "password": "123456"},
        {"username": "luis@correo.com", "password": "short"},
    ]

    for i, caso in enumerate(casos_prueba, 1):
        username = caso["username"]
        password = caso["password"]
        print(f"\nCaso {i}: usuario='{username}', contraseña='{password}'")
        try:
            mensaje = auth.login(username, password)
            print("✅", mensaje)
        except AuthError as e:
            print("❌ Error:", e)

if __name__ == "__main__":
    probar_login()