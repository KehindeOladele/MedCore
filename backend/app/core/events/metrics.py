from app.core.supabase_admin import supabase_admin


# -----------------------------
# EVENT SYSTEM METRICS
# -----------------------------
def get_event_metrics():

    events = (
        supabase_admin
        .table("events")
        .select("status, retry_count, event_type")
        .execute()
        .data
    )

    total = len(events)

    metrics = {
        "total_events": total,
        "processed": 0,
        "pending": 0,
        "failed": 0,
        "dead": 0,
        "success_rate": 0.0,
        "avg_retries": 0.0,
        "retry_exhausted": 0,
    }

    total_retries = 0

    for e in events:

        status = e.get("status")

        if status == "processed":
            metrics["processed"] += 1
        elif status == "pending":
            metrics["pending"] += 1
        elif status == "failed":
            metrics["failed"] += 1
        elif status == "dead":
            metrics["dead"] += 1
            metrics["retry_exhausted"] += 1

        total_retries += e.get("retry_count", 0)

    # -----------------------------
    # DERIVED METRICS
    # -----------------------------
    if total > 0:
        metrics["success_rate"] = (
            metrics["processed"] / total * 100
        )

        metrics["avg_retries"] = total_retries / total

    return metrics