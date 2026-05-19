import os

from backend.repositories.csv_user_repository import CsvUserRepository

from backend.services.auth_service import AuthService
from backend.services.chat_service import ChatService
from backend.services.file_service import FileUploadService

from backend.strategies.rule_based_chat_strategy import (
    RuleBasedChatStrategy
)

from backend.strategies.ai_chat_strategy import (
    AIChatStrategy
)

from backend.decorators.validation_chat_decorator import (
    ValidationChatDecorator
)

from backend.decorators.audit_chat_decorator import (
    AuditChatDecorator
)

from backend.observers.event_manager import EventManager

from backend.observers.audit_observer import AuditObserver

from backend.observers.document_index_observer import (
    DocumentIndexObserver
)


class AppServiceFactory:

    @staticmethod
    def create_user_repository():

        return CsvUserRepository()

    @staticmethod
    def create_auth_service():

        repository = (
            AppServiceFactory.create_user_repository()
        )

        return AuthService(repository)

    @staticmethod
    def create_chat_strategy():

        provider = os.getenv(
            "CHATBOT_PROVIDER",
            "rules"
        )

        if provider == "ai":
            return AIChatStrategy()

        return RuleBasedChatStrategy()

    @staticmethod
    def create_chat_service():

        strategy = (
            AppServiceFactory.create_chat_strategy()
        )

        service = ChatService(strategy)

        service = ValidationChatDecorator(service)

        service = AuditChatDecorator(service)

        return service

    @staticmethod
    def create_file_service(upload_dir: str):

        event_manager = EventManager()

        event_manager.subscribe(
            AuditObserver()
        )

        event_manager.subscribe(
            DocumentIndexObserver()
        )

        return FileUploadService(
            upload_dir,
            event_manager
        )