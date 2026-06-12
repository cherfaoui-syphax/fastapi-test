import pytest
import json
from unittest.mock import MagicMock, patch
from src.date_time_event_store.event_store_subscribers.event_manager import EventManager
from src.date_time_event_store.event_store_subscribers.console_listener import ConsoleEventHandler
from src.date_time_event_store.event_store_subscribers.http_listener import HttpEventHandler
from src.date_time_event_store.event_store_subscribers.rabbit_mq_listener import RabbitMQEventHandler

def test_event_handler_manager():
    manager = EventManager()
    
    mock_listener = MagicMock()
    manager.subscribe(mock_listener)
    
    # Notify event
    manager.notify(1780272000.0, "some_data")
    mock_listener.handle_event.assert_called_once_with(1780272000.0, "some_data")
    
    # Unsubscribe
    mock_listener.reset_mock()
    manager.unsubscribe(mock_listener)
    manager.notify(1780272000.0, "some_data")
    mock_listener.handle_event.assert_not_called()

def test_console_event_handler():
    handler = ConsoleEventHandler()
    with patch("builtins.print") as mock_print:
        handler.handle_event(1780272000.0, "test")
        mock_print.assert_called_once_with("Date: 1780272000.0, Data: test")

def test_http_event_handler():
    handler = HttpEventHandler("http://example.com/events")
    with patch("requests.post") as mock_post:
        handler.handle_event(1780272000.0, "test")
        mock_post.assert_called_once_with(
            "http://example.com/events", 
            json={"date": 1780272000.0, "data": "test"}
        )

def test_rabbitmq_event_handler():
    mock_connection = MagicMock()
    handler = RabbitMQEventHandler(mock_connection)
    
    # Test handle_event with connection
    handler.handle_event(1780272000.0, "test")
    expected_payload = json.dumps({"date": 1780272000.0, "data": "test"})
    mock_connection.publish.assert_called_once_with("test-queue", expected_payload)

def test_rabbitmq_event_handler_no_connection():
    # Test handle_event with None connection (should not raise exception)
    handler = RabbitMQEventHandler(None)
    handler.handle_event(1780272000.0, "test") # Should pass without raising error
