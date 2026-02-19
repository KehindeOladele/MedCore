<<<<<<< HEAD
-- Create laboratory file storage for Patients
=======
-- Create lab_results table to store lab test results, 
-- including file storage for results and associated metadata.
>>>>>>> sql
create table if not exists public.lab_results (
    id uuid primary key default gen_random_uuid(),

    patient_id uuid references patients(id),
    clinician_id uuid references practitioners(id),

    test_name text,
    status text check (status in ('pending','completed','reviewed')),

    result_data jsonb,
    file_url text,

    performed_at timestamp,
    created_at timestamp default now()
);
