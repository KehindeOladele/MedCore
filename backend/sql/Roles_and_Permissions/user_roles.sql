-- SQL script to create a roles table
create table roles (
    id uuid primary key default gen_random_uuid(),
    name text not null,
    organization_id uuid references organization(id) on delete cascade,
    role_type text check (role_type in ('system', 'organization')) default 'organization',
    is_active boolean default true,
    created_at timestamptz default now(),
    updated_at timestamptz default now(),
    description text,
    unique (name, organization_id)
);

--  Add RLS to roles
alter table roles enable row level security;

-- Allow super_adim to see roles of their organization or system-level roles
create policy "Org members can view roles"
on roles
for select
using (
    -- Users can see roles of their organization
    exists (
        select 1
        from user_roles ur
        where ur.user_id = auth.uid()
        and ur.organization_id = roles.organization_id
    )

    -- OR system-level roles can see everything
    or exists (
        select 1
        from user_roles ur
        join roles r2 on ur.role_id = r2.id
        where ur.user_id = auth.uid()
        and r2.role_type = 'system'
    )
);

-- Auto-update the updated_at timestamp on row modification
create or replace function update_updated_at_column()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

create trigger update_roles_updated_at
before update on roles
for each row
execute function update_updated_at_column();