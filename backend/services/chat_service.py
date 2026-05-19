class ChatService:

    def __init__(self, strategy):
        self.strategy = strategy

    def send_message(self, message: str) -> str:
        return self.strategy.generate_response(message)