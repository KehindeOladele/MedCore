create table audit_logs (
    id uuid default gen_random_uuid(),
    user_id uuid,
    action text,
    resource text,
    resource_id uuid,
    metadata jsonb,
    created_at timestamptz default now()
);
