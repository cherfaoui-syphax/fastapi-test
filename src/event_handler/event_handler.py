from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class AbstractEventHandler(ABC):
    """
    Abstract base class for event handlers.
    """
    @abstractmethod
    def handle_event(self, date: float, data: str) -> None:
        """
        Handle an event.
        
        Args:
            date (float): The date of the event.
            data (str): The data of the event.
        """
        pass

class EventHandlerManager:
    def __init__(self):
        self._listeners: list[AbstractEventHandler] = []

    def subscribe(self, listener: AbstractEventHandler) -> None:
        self._listeners.append(listener)

    def unsubscribe(self, listener: AbstractEventHandler) -> None:
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
