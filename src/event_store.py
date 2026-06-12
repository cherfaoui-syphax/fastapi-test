from .event_storage.storage_strategy import StorageStrategy
from .event_handler.event_handler import EventHandlerManager

class DateTimeEventStore:
    def __init__(self, storage_strategy: StorageStrategy, event_dispatcher: EventHandlerManager):
        self.storage_strategy = storage_strategy
        self.event_dispatcher = event_dispatcher

    def store_event(self, date: float, data: str) -> None:
        """
        Store an event and notify all listeners.
        
        Args:
            date (float): The date of the event in timestamp format.
            data (str): The data of the event.
        """
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
        return self.storage_strategy.get_events(start_date, end_date)

    def get_all_events(self) -> list[dict]:
        """
        Get all events.
        
        Returns:
            list[dict]: A list of all events.
        """
        return self.storage_strategy.get_events(0.0, 4102444800.0)
