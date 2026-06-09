from app.core.events.registry import EVENT_HANDLERS


#  ----- Event Dispatcher -----
def dispatch_event(event: dict):

    event_type = event["event_type"]

    handler = EVENT_HANDLERS.get(event_type)

    if not handler:
        return

    handler(event)