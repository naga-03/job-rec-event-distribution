class EventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type: str, handler):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def publish(self, event_type: str, payload: dict):
        handlers = self._subscribers.get(event_type, [])
        for handler in handlers:
            handler(payload)


event_bus = EventBus()
