-- SQL script to create a roles table
create table roles (
    id uuid primary key default gen_random_uuid(),
    name text unique (name, organization_id) not null,  -- org_admin, practitioners, staff, super_admin 
    organization_id uuid references organization(id) on delete cascade,
    role_type text check (role_type in ('system', 'organization')) default 'organization',
    is_active boolean default true,
    created_at timestamptz default now(),
    updated_at timestamptz default now(),
    description text
);