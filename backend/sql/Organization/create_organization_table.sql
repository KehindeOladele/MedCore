-- Create a table for healthcare organizations such as hospitals, clinics, and labs.
create table if not exists public.organizations (
    id uuid primary key default gen_random_uuid(),

    name text not null,
    type text check (
        type in (
            'tertiary_hospital',
            'secondary_hospital',
            'private_hospital',
            'primary_health_center',
            'clinic',
            'pharmacy',
            'private_laboratory',
            'pmv'
        )
    ),

    license_number text,
    phone text,
    email text,
    address text,

    state text,
    country text default 'Nigeria',

    logo_url text,

    active boolean default true,
    created_at timestamp default now()
);
