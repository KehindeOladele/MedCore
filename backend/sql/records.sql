create table if not exists public.medical_records (
    id uuid default gen_random_uuid() primary key,

    patient_id uuid references public.patients(id) on delete cascade,
    clinician_id uuid references auth.users(id),

    record_type text not null, -- observation | condition | medication
    recorded_at timestamp with time zone default timezone('utc', now()),

    -- FHIR-compliant resource
    clinical_data jsonb not null,

    created_at timestamp with time zone default timezone('utc', now())
);


-- Enable RLS
alter table public.medical_records enable row level security;


-- Patient can read own records
create policy "Patients read own records"
on public.medical_records
for select
using (auth.uid() = patient_id);


-- Clinicians can insert
create policy "Clinicians insert records"
on public.medical_records
for insert
with check (auth.uid() = clinician_id);


-- Enable RLS
-- alter table public.medical_records enable row level security;

-- Patients can read their own records
-- create policy "Patients can read own medical records"
-- on public.medical_records
-- for select
-- using (auth.uid() = patient_id);

-- -- Clinicians can create records
-- create policy "Clinicians can create medical records"
-- on public.medical_records
-- for insert
-- with check (auth.uid() = clinician_id);

