import logging
from .event_handler import AbstractEventHandler

logger = logging.getLogger(__name__)

class ConsoleEventHandler(AbstractEventHandler):
    def handle_event(self, date: float, data: str) -> None:
        # Code to handle console events
        logger.info(f"ConsoleEventHandler: Processing event with date={date}, data={repr(data)}")
        print(f"Date: {date}, Data: {data}")