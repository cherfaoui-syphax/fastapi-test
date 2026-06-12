import logging

from .abstract_listener import AbstractEventListener

logger = logging.getLogger(__name__)


class EventManager:
    def __init__(self):
        self._listeners: list[AbstractEventListener] = []

    def subscribe(self, listener: AbstractEventListener) -> None:
        self._listeners.append(listener)

    def unsubscribe(self, listener: AbstractEventListener) -> None:
        if listener in self._listeners:
            self._listeners.remove(listener)

    def notify(self, date: float, data: str) -> None:
        for listener in self._listeners:
            try:
                logger.info(f"Calling event handler: {listener.__class__.__name__} with date={date}, data={repr(data)}")
                listener.handle_event(date, data)
                logger.info(f"Event handler {listener.__class__.__name__} completed successfully")
            except Exception as e:
                logger.error(f"Error executing event handler {listener.__class__.__name__}: {e}", exc_info=True)
