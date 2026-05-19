from datetime import datetime

class AuditChatDecorator:

    def __init__(self, component):
        self.component = component

    def send_message(self, message: str) -> str:

        response = self.component.send_message(message)

        print({
            "event": "chat_message",
            "message": message,
            "response": response,
            "created_at": datetime.now().isoformat()
        })

        return response