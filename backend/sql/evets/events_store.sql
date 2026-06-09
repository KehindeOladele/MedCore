-- Event store for agreggate Actions 
create table if not exists events (
    id uuid primary key default gen_random_uuid(),

    aggregate_type text not null,   -- patient | practitioner | organization
    aggregate_id uuid not null,

    event_type text not null,       -- onboarding.email_sent etc

    payload jsonb not null default '{}'::jsonb,

    status text not null default 'pending',   -- pending | processed | failed

    created_at timestamptz not null default now(),

    retry_count INTEGER DEFAULT 0,
    last_attempt_at TIMESTAMPTZ,
    failure_reason TEXT,
    processed_at TIMESTAMPTZ,
);