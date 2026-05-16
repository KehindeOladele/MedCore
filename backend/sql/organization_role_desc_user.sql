-- alter table roles add column if not exists description text;

-- alter table user_roles add column if not exists organization_id uuid;

-- Add organization_id
alter table roles
add column if not exists organization_id uuid references organizations(id) on delete cascade;

-- Add role_type
alter table roles
add column if not exists role_type text 
check (role_type in ('system', 'organization')) 
default 'organization';

-- Add is_active
alter table roles
add column if not exists is_active boolean default true;

-- Add timestamps
alter table roles
add column if not exists created_at timestamptz default now();

alter table roles
add column if not exists updated_at timestamptz default now();

-- Add composite unique constraint
alter table roles
add constraint roles_name_org_unique
unique (name, organization_id);