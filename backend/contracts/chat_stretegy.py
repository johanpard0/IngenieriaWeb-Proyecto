from typing import Protocol

class ChatStrategy(Protocol):

    def generate_response(self, message: str) -> str:
        pass