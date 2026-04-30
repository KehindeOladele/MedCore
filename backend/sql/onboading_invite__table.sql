-- ----- Onboarding Invitation Table -----
create table invitations (
    id uuid primary key default gen_random_uuid(),
    email text not null,
    organization_id uuid references organizations(id) on delete cascade,
    role_name text not null,
    invited_by uuid references auth.users(id),
    token text unique not null,
    status text check (status in ('pending', 'accepted', 'expired')) default 'pending',
    expires_at timestamptz,
    created_at timestamptz default now()
);