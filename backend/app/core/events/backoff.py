from datetime import datetime, timedelta, timezone


# ----- Event Retry Scheduling -----
def compute_backoff(retry_count: int) -> timedelta:
    """
    Exponential backoff strategy:
    1st retry → 2s
    2nd retry → 4s
    3rd retry → 8s
    4th retry → 16s
    capped later in processor
    """

    seconds = 2 ** retry_count
    return timedelta(seconds=seconds)


def compute_next_retry_at(retry_count: int) -> str:
    delay = compute_backoff(retry_count)

    return (
        datetime.now(timezone.utc)
        + delay
    ).isoformat()