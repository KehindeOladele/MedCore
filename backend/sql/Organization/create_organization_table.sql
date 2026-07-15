-- Create a table for healthcare organizations such as hospitals, clinics, and labs.
create table if not exists public.organizations (
    id uuid primary key default gen_random_uuid(),

    name text not null,
    type text check (
        type in (
            'tertiary_hospital',
            'secondary_hospital',
            'private_hospital',
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

    state text,
    country text default 'Nigeria',

    logo_url text,

    active boolean default true,
    created_at timestamp default now()

    -- Onboarding columns
    onboarding_status text DEFAULT 'pending',
    onboarding_email_sent boolean DEFAULT false,
    onboarding_email_sent_at timestamptz,
    onboarding_completed boolean DEFAULT false,
    onboarding_completed_at timestamptz,
    onboarding_retry_count integer DEFAULT 0,
    onboarding_last_attempt_at timestamptz,
    onboarding_last_error text,
    onboarding_failure_reason text;
);
