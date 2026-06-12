from .event_storage_strategy.abstract_strategy import StorageStrategy
from .event_store_subscribers.event_manager import EventManager

class DateTimeEventStore:
    def __init__(self, storage_strategy: StorageStrategy, event_dispatcher: EventManager):
        self.storage_strategy = storage_strategy
        self.event_dispatcher = event_dispatcher

    
    def _validate_date(self, date: float) -> None:
        if date < 0 or date > 4102444800.0:
            raise ValueError("Invalid date")

    def store_event(self, date: float, data: str) -> None:
        """
        Store an event and notify all listeners.
        
        Args:
            date (float): The date of the event in timestamp format.
            data (str): The data of the event.
        """
        self._validate_date(date)
        self.storage_strategy.store_event(date, data)
        self.event_dispatcher.notify(date, data)

    def get_events(self, start_date: float, end_date: float) -> list[dict]:
        """
        Get events in a date range.
        
        Args:
            start_date (float): The start date of the range in timestamp format.
            end_date (float): The end date of the range in timestamp format.
        
        Returns:
            list[dict]: A list of events in the date range.
        """
        self._validate_date(start_date)
        self._validate_date(end_date)
        if start_date > end_date:
            raise ValueError("Start date must be before end date")
        return self.storage_strategy.get_events(start_date, end_date)

    def get_all_events(self) -> list[dict]:
        """
        Get all events.
        
        Returns:
            list[dict]: A list of all events.
        """
        return self.storage_strategy.get_events(0.0, 4102444800.0)
