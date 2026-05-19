from fastapi import HTTPException

class ValidationChatDecorator:

    def __init__(self, component):
        self.component = component

    def send_message(self, message: str) -> str:

        if not message or not message.strip():
            raise HTTPException(
                status_code=400,
                detail="El mensaje no puede estar vacío"
            )

        return self.component.send_message(message)