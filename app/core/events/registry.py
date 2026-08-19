EVENT_HANDLERS = {}


# ----- Register Event -----
def register(event_type: str):
    """Handlers self-register"""
    def decorator(func):

        if event_type in EVENT_HANDLERS:

            raise ValueError(
                f"Handler already "
                f"registered for "
                f"{event_type}"
            )
        
        EVENT_HANDLERS[event_type] = func
        
        return func
    return decorator