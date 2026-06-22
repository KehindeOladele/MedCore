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

    replayed BOOLEAN DEFAULT FALSE,
    replayed_at TIMESTAMPTZ,
    replayed_by UUID,

    failed_at TIMESTAMPTZ DEFAULT NOW()
);