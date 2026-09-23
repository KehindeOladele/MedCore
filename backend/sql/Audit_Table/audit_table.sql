-- Query to Create Audit table
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    actor_id UUID,
    actor_type TEXT,

    action TEXT NOT NULL,

    resource_type TEXT NOT NULL,
    resource_id TEXT NOT NULL,

    metadata JSONB DEFAULT '{}'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Add Supabase Row Level Security
ALTER TABLE audit_logs
ENABLE ROW LEVEL SECURITY;