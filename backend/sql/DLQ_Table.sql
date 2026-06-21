-- Dead Letter Queue (DLQ) Table
-- Table for Dead events
CREATE TABLE IF NOT EXISTS events_dead_letter (
    id UUID PRIMARY KEY,
    original_event_id UUID,
    
    aggregate_type TEXT,
    aggregate_id TEXT,
    event_type TEXT,
    payload JSONB,

    retry_count INT,
    failure_reason TEXT,

    failed_at TIMESTAMPTZ DEFAULT NOW()
);