--  Create Prescription Table
create table prescriptions (
    id uuid primary key default gen_random_uuid(),
    patient_id uuid not null,
    drug_name text,
    category text,
    dosage text,
    instructions text,
    start_date date,
    end_date date,
    status text,
    created_at timestamp default now()
);
