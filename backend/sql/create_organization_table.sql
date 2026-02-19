-- Create Organizations Table
create table if not exists public.organizations (
    id uuid primary key default gen_random_uuid(),

    name text not null,
    type text, -- hospital, clinic, lab

    phone text,
    email text,
    address text,

    active boolean default true,
    created_at timestamp default now()
);
