import pytest
from unittest.mock import MagicMock
from src.date_time_event_store.event_storage_strategy.in_memory_strategy import InMemoryStorageStrategy
from src.date_time_event_store.event_storage_strategy.mongo_db_strategy import MongoDBStorageStrategy

def test_in_memory_storage_strategy():
    strategy = InMemoryStorageStrategy()
    
    # Store some events
    strategy.store_event(1780272000.0, "one")
    strategy.store_event(1780444800.0, "three")
    strategy.store_event(1780358400.0, "two")

    # Test get_events sorted order
    events = strategy.get_events(1780272000.0, 1780444800.0)
    assert len(events) == 3
    assert events[0] == {"date": 1780272000.0, "data": "one"}
    assert events[1] == {"date": 1780358400.0, "data": "two"}
    assert events[2] == {"date": 1780444800.0, "data": "three"}

    # Test filtering date range
    filtered = strategy.get_events(1780358400.0, 1780358400.0)
    assert len(filtered) == 1
    assert filtered[0]["date"] == 1780358400.0

    # Test stream
    stream = strategy.get_events_stream(1780272000.0, 1780358400.0)
    stream_list = list(stream)
    assert len(stream_list) == 2
    assert stream_list[0]["date"] == 1780272000.0
    assert stream_list[1]["date"] == 1780358400.0



# Ce test me fait vraiment poser la question  "est ce que je test mon code ou estce que je test un mock ??"
# J'aurais probablement soulevé ce point pendant un code review.
# 
# 
def test_mongodb_storage_strategy():
    # Mock MongoDB connection structure: connection[db_name][collection_name]
    mock_connection = MagicMock()
    mock_db = MagicMock()
    mock_collection = MagicMock()
    
    mock_connection.__getitem__.return_value = mock_db
    mock_db.__getitem__.return_value = mock_collection

    strategy = MongoDBStorageStrategy(mock_connection, "test_db", "test_col")

    # Test store_event
    strategy.store_event(1780272000.0, "hello")
    
    # Verify connection access
    mock_connection.__getitem__.assert_called_with("test_db")
    mock_db.__getitem__.assert_called_with("test_col")
    
    mock_collection.insert_one.assert_called_once_with({
        "date": 1780272000.0,
        "data": "hello"
    })

    # Test get_events
    mock_collection.find.return_value = [
        {"date": 1780272000.0, "data": "hello"}
    ]
    events = strategy.get_events(1780272000.0, 1780358400.0)
    mock_collection.find.assert_called_with({
        "date": {
            "$gte": 1780272000.0,
            "$lte": 1780358400.0
        }
    },{'_id': 0})
    assert events == [{"date": 1780272000.0, "data": "hello"}]

    # Test get_events_stream
    mock_collection.find.reset_mock()
    mock_collection.find.return_value = iter([
        {"date": 1780272000.0, "data": "hello"}
    ])
    stream = strategy.get_events_stream(1780272000.0, 1780358400.0)
    assert list(stream) == [{"date": 1780272000.0, "data": "hello"}]
