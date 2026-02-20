-- Create a table for healthcare organizations such as hospitals, clinics, and labs.
create table if not exists public.organizations (
    id uuid primary key default gen_random_uuid(),

    name text not null,
    type text check (
        type in (
            'tertiary_hospital',
            'secondary_hospital',
            'clinic',
            'pharmacy',
            'laboratory',
            'phc',
            'pmv'
        )
    ),

    license_number text,
    phone text,
    email text,
    address text,

    active boolean default true,
    created_at timestamp default now()
);
