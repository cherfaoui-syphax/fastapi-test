from typing import Iterator
from abc import ABC, abstractmethod

class StorageStrategy(ABC):
    """
    Abstract base class for storage strategies.
    """
    @abstractmethod
    def store_event(self, date: float, data: str) -> None:
        """
        Store an event.
        
        Args:
            date (float): The date of the event in timestamp format.
            data (str): The data of the event.
        """
        pass

    @abstractmethod
    def get_events(self, start_date: float, end_date: float) -> list[dict]:
        """
        Get events in a date range.
        
        Args:
            start_date (float): The start date of the range in timestamp format.
            end_date (float): The end date of the range in timestamp format.
        
        Returns:
            list[dict]: A list of events in the date range.
        """
        pass
    
    @abstractmethod
    def get_events_stream(self, start_date: float, end_date: float) -> Iterator[dict]:
        """
        Get events in a date range as a stream.
        
        Args:
            start_date (float): The start date of the range in timestamp format.
            end_date (float): The end date of the range in timestamp format.
        
        Returns:
            Iterator[dict]: An iterator of events in the date range.
        """
        pass
