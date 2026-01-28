-- Query to create a table for clinicians
create table clinicians (
    id uuid primary key,
    user_id uuid references auth.users(id),
    role text,
    created_at timestamptz default now()
);
