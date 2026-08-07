-- Create Patient Access Grants Table
-- Admin assignment
-- Patient approval
-- Temporary access
-- OTP verification

create table patient_access_grants (
    id uuid primary key default gen_random_uuid(),

    patient_id uuid references patients(id),
    practitioner_id uuid references practitioners(id),

    organization_id uuid references organizations(id),

    access_type text check (
        access_type in ('assigned','patient_granted','emergency')
    ),

    status text check (
        status in ('pending','approved','revoked')
    ),

    granted_at timestamp,
    expires_at timestamp,

    created_at timestamp default now()
);
