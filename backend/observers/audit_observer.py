from datetime import datetime

class AuditObserver:

    def update(self, event_name: str, data: dict):

        print({
            "event": event_name,
            "data": data,
            "created_at": datetime.now().isoformat()
        })