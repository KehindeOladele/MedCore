-- Dead Letter Queue (DLQ) Table
-- Table for Dead events
CREATE TABLE IF NOT EXISTS events_dead_letter (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    original_event_id UUID NOT NULL,
    
    aggregate_type TEXT NOT NULL,
    aggregate_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload JSONB,

    retry_count INT NOT NULL,
    failure_reason TEXT NOT NULL,

    replayed BOOLEAN DEFAULT FALSE NOT NULL,
    replayed_at TIMESTAMPTZ NOT NULL,
    replayed_by UUID,

    failed_at TIMESTAMPTZ DEFAULT NOW()
);
