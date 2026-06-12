from .event_storage_strategy.abstract_strategy import StorageStrategy
import os
from .event_storage_strategy import MongoDBStorageStrategy, InMemoryStorageStrategy
from .event_store_subscribers import HttpEventHandler, RabbitMQEventHandler, ConsoleEventHandler, EventManager
from .event_store import DateTimeEventStore
from typing import Literal, List
class EventStoreFactory:
    def __init__(self, storage_type : Literal["mongodb", "in_memory"], event_handlers : List[Literal["http", "rabbitmq", "console"]], mongo_connection=None, rabbitmq_connection=None, http_endpoint=None):
        self.storage_type = storage_type
        self.event_handlers = event_handlers
        self.mongo_connection = mongo_connection
        self.rabbitmq_connection = rabbitmq_connection
        self.http_endpoint = http_endpoint

    def create_storage_strategy(self) -> StorageStrategy:
        if self.storage_type is None:
            raise ValueError("Storage type is not specified")

        if self.storage_type == "in_memory":
            return InMemoryStorageStrategy()

        if self.storage_type == "mongodb":
            if self.mongo_connection is None:
                raise ValueError("Mongo connection is not specified")
            db_name = os.getenv("MONGO_DB_NAME", "event_store")
            collection_name = os.getenv("MONGO_COLLECTION_NAME", "events")
            return MongoDBStorageStrategy(self.mongo_connection, db_name, collection_name)
        
        raise ValueError("Invalid storage type")



    def create_event_handlers(self) -> EventManager:
        dispatcher = EventManager()
        for handler_type in self.event_handlers:
            if handler_type == "http":
                if self.http_endpoint:
                    dispatcher.subscribe(HttpEventHandler(self.http_endpoint))
                else:
                    raise ValueError("HTTP endpoint is not specified")
            elif handler_type == "rabbitmq":
                if self.rabbitmq_connection:
                    dispatcher.subscribe(RabbitMQEventHandler(self.rabbitmq_connection))
                else:
                    raise ValueError("RabbitMQ connection is not specified")
            elif handler_type == "console":
                dispatcher.subscribe(ConsoleEventHandler())
            else:
                raise ValueError("Invalid handler type")
        return dispatcher

    def create_event_store(self) -> DateTimeEventStore:
        return DateTimeEventStore(
            storage_strategy=self.create_storage_strategy(),
            event_dispatcher=self.create_event_handlers()
        )
