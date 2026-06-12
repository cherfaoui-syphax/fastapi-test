from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class AbstractEventListener(ABC):
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

