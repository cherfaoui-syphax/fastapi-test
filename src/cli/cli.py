import os
import datetime
import json
import typer
import logging
from dotenv import load_dotenv
from src.event_store_factory import EventStoreFactory

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = typer.Typer(help="Event Store CLI Utility")

def get_event_store():
    # Load configuration from environment variables or defaults
    storage_type = os.getenv("STORAGE_TYPE", "in_memory")
    
    if storage_type not in ["mongodb", "in_memory"]:
        raise ValueError(f"Invalid storage type: {storage_type}")
    
    mongo_connection = None
    if storage_type == "mongodb":
        from src.utils.mongo_db import MongoDb
        try:
            mongo_db_util = MongoDb()
            mongo_connection = mongo_db_util.conn
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB ({e.__class__.__name__}: {e})")
            raise
    

    handlers_env = os.getenv("EVENT_HANDLERS", "console")
    event_handlers = [h.strip() for h in handlers_env.split(",") if h.strip()]

    rabbitmq_connection = None
    # Initialize RabbitMQ connection if configured
    if "rabbitmq" in event_handlers:
        from src.utils.rabbit_mq import RabbitMQ
        try:
            rabbitmq_connection = RabbitMQ()
        except Exception as e:
            print(f"Warning: Failed to connect to RabbitMQ ({e.__class__.__name__}: {e})")
            if "rabbitmq" in event_handlers:
                event_handlers.remove("rabbitmq")

    event_store_factory = EventStoreFactory(
        storage_type=storage_type,
        event_handlers=event_handlers,
        mongo_connection=mongo_connection,
        rabbitmq_connection=rabbitmq_connection,
        http_endpoint=os.getenv("HTTP_ENDPOINT")
    )
    return event_store_factory.create_event_store()

def _store_event(event_store, date: str, message: str):
    date_timestamp = datetime.datetime.strptime(date, "%Y-%m-%d").timestamp()
    event_store.store_event(date_timestamp, message)
    print(f"Success: Event added for {date} - '{message}'")

def _add_multiple_events(event_store, n: int):
    for i in range(n):
        date_timestamp = datetime.datetime.now().timestamp()
        event_store.store_event(date_timestamp, f"Event {i}")
        print(f"Added event {i}")

def _get_events(event_store, start_date: str, end_date: str):
    start_ts = datetime.datetime.strptime(start_date, "%Y-%m-%d").timestamp()
    end_ts = datetime.datetime.strptime(end_date, "%Y-%m-%d").timestamp()
    events = event_store.storage_strategy.get_events(start_ts, end_ts)
    print(f"Events from {start_date} to {end_date}: {events}")

def _get_all_events(event_store):
    events = event_store.get_all_events()
    print(f"All events:\n", *events , sep="\n")

def _export_as_jsonl(event_store, output_file: str):
    events = event_store.get_all_events()
    with open(output_file, "w") as f:
        for event in events:
            # Convert BSON ObjectId to string for JSON serialization only for MongoDB
            if "_id" in event:
                event = dict(event)
                event["_id"] = str(event["_id"])
            f.write(json.dumps(event) + "\n")
    print(f"Success: Exported {len(events)} events to {output_file}")

@app.command()
def store_event(
    date: str = typer.Option(None, "--date", "-d", prompt="Enter event date (YYYY-MM-DD)"),
    message: str = typer.Option(None, "--message", "-m", prompt="Enter event message")
):
    """Add an event to the event store"""
    try:
        _store_event(get_event_store(), date, message)
    except Exception as e:
        print(f"Error: {e}")

@app.command()
def add_multiple_events(
    n: int = typer.Option(None, "--count", "-c", prompt="Enter number of events to add")
):
    """Add multiple events to the event store"""
    try:
        _add_multiple_events(get_event_store(), n)
    except Exception as e:
        print(f"Error: {e}")

@app.command()
def get_events(
    start_date: str = typer.Option(None, "--start-date", "-s", prompt="Enter start date (YYYY-MM-DD)"),
    end_date: str = typer.Option(None, "--end-date", "-e", prompt="Enter end date (YYYY-MM-DD)")
):
    """Get events within a specific date range"""
    try:
        _get_events(get_event_store(), start_date, end_date)
    except Exception as e:
        print(f"Error: {e}")

@app.command()
def get_all_events():
    """Get all events"""
    try:
        _get_all_events(get_event_store())
    except Exception as e:
        print(f"Error: {e}")

@app.command()
def export_as_jsonl(
    output_file: str = typer.Option("exported_events.jsonl", "--output", "-o", prompt="Enter output JSONL file path")
):
    """Export all events to a JSONL file"""
    try:
        _export_as_jsonl(get_event_store(), output_file)
    except Exception as e:
        print(f"Error: {e}")

@app.command()
def interactive():
    """Start an interactive command session menu"""
    print("\n--- Event Store Interactive CLI ---")
    event_store = get_event_store()
    while True:
        print("\nChoose an option:")
        print("1. Add event")
        print("2. Add multiple events")
        print("3. View events in date range")
        print("4. View all events")
        print("5. Export events as JSONL")
        print("6. Exit")
        
        choice = typer.prompt("Enter option number (1-6)")
        try:
            if choice == "1":
                date = typer.prompt("Enter date (YYYY-MM-DD)")
                message = typer.prompt("Enter message")
                _store_event(event_store, date, message)
            elif choice == "2":
                count = typer.prompt("Enter count", type=int)
                _add_multiple_events(event_store, count)
            elif choice == "3":
                start = typer.prompt("Enter start date (YYYY-MM-DD)")
                end = typer.prompt("Enter end date (YYYY-MM-DD)")
                _get_events(event_store, start, end)
            elif choice == "4":
                _get_all_events(event_store)
            elif choice == "5":
                out = typer.prompt("Enter output path", default="exported_events.jsonl")
                _export_as_jsonl(event_store, out)
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid option.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    app()