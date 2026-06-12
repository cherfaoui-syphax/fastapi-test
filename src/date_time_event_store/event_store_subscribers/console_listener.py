import logging
from .abstract_listener import AbstractEventListener

logger = logging.getLogger(__name__)

class ConsoleEventHandler(AbstractEventListener):
    def handle_event(self, date: float, data: str) -> None:
        # Code to handle console events
        logger.info(f"ConsoleEventHandler: Processing event with date={date}, data={repr(data)}")
        print(f"Date: {date}, Data: {data}")