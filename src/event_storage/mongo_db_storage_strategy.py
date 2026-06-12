import logging
from typing import Iterator
from .storage_strategy import StorageStrategy

logger = logging.getLogger(__name__)

class MongoDBStorageStrategy(StorageStrategy):
    def __init__(self, connection, database_name: str, collection_name: str):
        self.connection = connection
        self.database_name = database_name
        self.collection_name = collection_name
        
    def store_event(self, date: float, data: str) -> None:
        #Save data to MongoDB
        logger.info(f"MongoDBStorageStrategy: Storing event in {self.database_name}.{self.collection_name} with date={date}, data={repr(data)}")
        self.connection[self.database_name][self.collection_name].insert_one({
            "date": date,
            "data": data
        })
        logger.info("MongoDBStorageStrategy: Successfully stored event")
        
    def get_events(self, start_date: float, end_date: float) -> list[dict]:
        #Load data from MongoDB
        logger.info(f"MongoDBStorageStrategy: Querying events from {self.database_name}.{self.collection_name} between start_date={start_date} and end_date={end_date}")
        # ignore id 
        events = list(self.connection[self.database_name][self.collection_name].find({
            "date": {
                "$gte": start_date,
                "$lte": end_date
            }
        },  {
        "_id": 0
    }))
        logger.info(f"MongoDBStorageStrategy: Retrieved {len(events)} events")
        return events
        
    def get_events_stream(self, start_date: float, end_date: float) -> Iterator[dict]:
        #Load data from MongoDB
        logger.info(f"MongoDBStorageStrategy: Requesting events stream from {self.database_name}.{self.collection_name} between start_date={start_date} and end_date={end_date}")
        return self.connection[self.database_name][self.collection_name].find({
            "date": {
                "$gte": start_date,
                "$lte": end_date
            } 
        },  {
        "_id": 0
    })
        
    

