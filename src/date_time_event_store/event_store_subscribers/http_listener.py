import requests
import logging
from .abstract_listener import AbstractEventListener

logger = logging.getLogger(__name__)

class HttpEventHandler(AbstractEventListener):
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        
    def handle_event(self, date: float, data: str) -> None:
        logger.info(f"HttpEventHandler: Sending POST request to endpoint {self.endpoint} with date={date}, data={repr(data)}")
        response = requests.post(self.endpoint, json={"date": date, "data": data})
        logger.info(f"HttpEventHandler: Received response with status_code={response.status_code}")
