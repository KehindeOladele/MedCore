EVENT_HANDLERS = {}


# ----- Register Event -----
def register(event_type: str):
    """Handlers self-register"""
    def decorator(func):
        EVENT_HANDLERS[event_type] = func
        return func
    return decorator