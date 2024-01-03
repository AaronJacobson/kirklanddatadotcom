import os

from azure.monitor.events.extension import track_event
from azure.monitor.opentelemetry import configure_azure_monitor
from dotenv import load_dotenv

load_dotenv()

configure_azure_monitor(connection_string=os.getenv("application_insights"))


def log_info(event_name: str, dimensions: dict):
    print("Logging:", event_name, dimensions)
    dimensions["type"] = "local_testing"
    track_event(
        event_name,
        dimensions,
    )
