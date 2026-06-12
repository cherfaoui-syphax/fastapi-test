import os
import logging
from pymongo import MongoClient

logger = logging.getLogger(__name__)


class MongoDb : 

    def __init__(self):

        self.uri = os.getenv("MONGO_DB_URI")
        if not self.uri:
            raise ValueError("MONGO_DB_URI environment variable is not set")
            
        self.db = os.getenv("MONGO_DB_NAME", "event_store")
        self.collection = os.getenv("MONGO_COLLECTION_NAME", "events")

        try:
            self.client = MongoClient(self.uri)
            # Send a ping to verify connection
            self.client.admin.command('ping')
            logger.info("Successfully established connection to MongoDB.")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
            
        self.db = self.client[self.db]
        self.collection = self.db[self.collection]
        

    @property
    def conn(self):
        if self.client is None:
            try:
                self.client = MongoClient(self.uri)
                self.client.admin.command('ping')
                logger.info("Successfully established connection to MongoDB.")
            except Exception as e:
                logger.error(f"Failed to connect to MongoDB: {e}")
                raise
        return self.client
