-- PATIENTS TABLE (JSONB-ENABLED)
-- Patients table with FHIR extensibility
create table if not exists public.patients (
    -- Identification
    id uuid primary key references auth.users(id) on delete cascade,
    medical_id text UNIQUE,

    -- Core relational fields
    first_name text,
    last_name text,
    date_of_birth date,
    gender text,
    blood_group text,

    -- Contact info (basic)
    phone text,

    -- FHIR extensibility
    fhir_metadata jsonb default '{}'::jsonb,

    created_at timestamp with time zone default timezone('utc', now())
);


-- Enable RLS
alter table public.patients enable row level security;


-- Policies
create policy "Patients can read own data"
on public.patients
for select
using (auth.uid() = id);


-- Create policy for inserting patient data
create policy "Patients can insert own data"
on public.patients
for insert
with check (auth.uid() = id);


-- Create policy for updating patient data
create policy "Patients can update own data"
on public.patients
for update
using (auth.uid() = id);


-- Create policy for Patients to read own record
create policy "Patients can read own record"
on public.patients
for select
using (auth.uid() = id);


-- Create policy for Patients to insert own record (TEMP) in to the medical rec table
create policy "Patients can create own records (TEMP)"
on public.medical_records
for insert
with check (auth.uid() = patient_id);



-- -- Create policy for Patients to insert own record
-- create policy "Patients can insert own record"
-- on public.patients
-- for insert
-- with check (auth.uid() = id);





-- NOT JSONB ENABLED
-- --  Create Patients Table
-- create table if not exists public.patients (
--     id uuid primary key references auth.users(id) on delete cascade,
--     date_of_birth date,
--     gender text,
--     blood_group text,
--     created_at timestamp with time zone default timezone('utc', now())
-- );


-- --  Enable Row Level Security (RLS)
-- alter table public.patients enable row level security;


-- --  Create Policies for Patients can View Own Record
-- create policy "Patients can view own record"
-- on public.patients
-- for select
-- using (auth.uid() = id);


-- --  Create Policies for Patients Table for Inserting Own Record
-- create policy "Patients can insert own record"
-- on public.patients
-- for insert
-- with check (auth.uid() = id);


-- Create PostgreSQL Sequence for Medical_id # DROPPED
-- CREATE SEQUENCE patient_medical_id_seq
-- START 1
-- INCREMENT 1;



-- National Scale Identifier System
-- | Resource          | Prefix |
-- | ----------------- | ------ |
-- | Patient           | P      |
-- | Practitioner      | PR     |
-- | Organization      | O      |
-- | Encounter         | E      |
-- | Appointment       | A      |
-- | Observation       | OBS    |
-- | Condition         | C      |
-- | MedicationRequest | MR     |
-- | Device            | D      |
-- | Claim             | CL     |
-- | Invoice           | INV    |

-- Example:
-- MC-NG-P-0000000001   (Patient)
-- MC-NG-O-0000000001   (Organization)
-- MC-NG-PR-0000000001  (Practitioner)
-- MC-NG-D-0000000001   (Device)

-- Where:

-- MC = MedCore
-- NG = Nigeria
-- P = Patient


-- Create Medical Id function
CREATE OR REPLACE FUNCTION generate_patient_medical_id()
RETURNS TEXT
LANGUAGE plpgsql
AS $$
DECLARE
    seq BIGINT;
BEGIN
    seq := nextval('patient_medical_id_seq');

    RETURN 'MC-NG-P-' || LPAD(seq::TEXT, 10, '0');
END;
$$;


-- Test if sequence exists
SELECT generate_medical_id();


-- Set Default
ALTER TABLE patients
ALTER COLUMN medical_id
SET DEFAULT generate_medical_id();


-- explicitly naming indexes is cleaner for large-scale systems.
CREATE UNIQUE INDEX IF NOT EXISTS idx_patients_medical_id
ON patients(medical_id);


-- Update Existing Patients
UPDATE patients
SET medical_id = generate_medical_id()
WHERE medical_id IS NULL;


-- FHIR Serialization Support
ALTER TABLE patients
ADD COLUMN IF NOT EXISTS identifier_system TEXT
DEFAULT 'https://api.medcore.africa/fhir/identifier/patient';

ALTER TABLE patients
ADD COLUMN IF NOT EXISTS identifier_use TEXT
DEFAULT 'official';