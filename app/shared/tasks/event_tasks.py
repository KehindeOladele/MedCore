from app.core.events.processor import process_pending_events


def process_events_task():
    process_pending_events()