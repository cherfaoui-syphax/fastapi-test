import logging
from typing import Iterator
from .abstract_strategy import StorageStrategy
from sortedcontainers import SortedList

logger = logging.getLogger(__name__)

class InMemoryStorageStrategy(StorageStrategy):
    def __init__(self):
        self.data = SortedList(key=lambda x: x[0])

    def store_event(self, date: float, data: str) -> None:
        logger.info(f"InMemoryStorageStrategy: Storing event with date={date}, data={repr(data)}")
        self.data.add((date, data))

    def get_events(self, start_date: float, end_date: float) -> list[dict]:
        logger.info(f"InMemoryStorageStrategy: Querying events between start_date={start_date} and end_date={end_date}")
        events = [ 
            {'at' : date, 'data' : data} for date, data in self.data.irange_key(start_date, end_date)
        ]
        logger.info(f"InMemoryStorageStrategy: Retrieved {len(events)} events")
        return events

    def get_events_stream(self, start_date: float, end_date: float) -> Iterator[dict]:
        logger.info(f"InMemoryStorageStrategy: Requesting events stream between start_date={start_date} and end_date={end_date}")
        for item in self.data.irange_key(start_date, end_date):
            yield {'at' : item[0], 'data' : item[1]}

    