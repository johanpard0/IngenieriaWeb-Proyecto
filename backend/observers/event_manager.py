class EventManager:

    def __init__(self):
        self.observers = []

    def subscribe(self, observer):
        self.observers.append(observer)

    def notify(self, event_name: str, data: dict):

        for observer in self.observers:
            observer.update(event_name, data)