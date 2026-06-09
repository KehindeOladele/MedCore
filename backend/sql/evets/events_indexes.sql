-- Event indexes
CREATE INDEX IF NOT EXISTS idx_events_type
ON events(event_type);

CREATE INDEX IF NOT EXISTS idx_events_aggregate
ON events(aggregate_type, aggregate_id);

CREATE INDEX IF NOT EXISTS idx_events_status
ON events(status);