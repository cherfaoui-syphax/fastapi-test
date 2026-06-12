import json
import logging
from .abstract_listener import AbstractEventListener

logger = logging.getLogger(__name__)

class RabbitMQEventHandler(AbstractEventListener):
    def __init__(self, connection):
        self.connection = connection
        
    def handle_event(self, date: float, data: str) -> None:
        # Code to handle RabbitMQ events
        if self.connection:
            payload = json.dumps({"date": date, "data": data})
            logger.info(f"RabbitMQEventHandler: Publishing event to queue 'event': {payload}")
            self.connection.publish("test-queue", payload)
            logger.info("RabbitMQEventHandler: Successfully published event")
        else:
            logger.warning("RabbitMQEventHandler: Cannot handle event, connection is not established")


