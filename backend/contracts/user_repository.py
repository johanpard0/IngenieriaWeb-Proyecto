from typing import Protocol

class UserRepository(Protocol):

    def find_by_username(self, username: str):
        pass

    def find_by_provider(self, provider: str, provider_id: str):
        pass

    def save(self, user: dict):
        pass