# ----- Event Processing Exception -----
class EventProcessingError(Exception):
    pass


# ----- Dipatch Event Exception -----
class EventDispatchError(
    EventProcessingError
):
    pass


# ----- Event Handlet Exception -----
class EventHandlerError(
    EventProcessingError
):
    pass