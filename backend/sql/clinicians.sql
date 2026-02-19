-- Query to create a table for clinicians
create table clinicians (
    id uuid primary key,
    user_id uuid references auth.users(id),
    role text,
    created_at timestamptz default now()
);

create table if not exists practitioners (
    id uuid primary key references auth.users(id) on delete cascade,
    user_id uuid references auth.users(id),
    first_name text not null,
    last_name text not null,
    role text,
    license_number text,
    specialty text,
    phone text,
    organization_id uuid references organizations(id),
    active boolean default true,
    created_at timestamp default now(),
    fhir_metadata jsonb default '{}'
);
