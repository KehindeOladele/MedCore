-- PATIENTS TABLE (JSONB-ENABLED)
-- Patients table with FHIR extensibility
-- create table if not exists public.patients (
--     id uuid primary key references auth.users(id) on delete cascade,

--     -- Core relational fields
--     first_name text,
--     last_name text,
--     date_of_birth date,
--     gender text,
--     blood_group text,

--     -- Contact info (basic)
--     phone text,

--     -- FHIR extensibility
--     fhir_metadata jsonb default '{}'::jsonb,

--     created_at timestamp with time zone default timezone('utc', now())
-- );

--- Create Patients Table with FHIR Metadata
create table if not exists public.patients (
    id uuid primary key references auth.users(id) on delete cascade,

    first_name text not null,
    last_name text not null,
    middle_name text,

    date_of_birth date not null,
    gender text check (gender in ('male','female','other','unknown')),

    blood_group text,
    marital_status text,

    phone text,
    email text,
    address text,

    emergency_contact_name text,
    emergency_contact_phone text,

    access_pin text, -- hashed
    organization_id uuid references organizations(id),

    active boolean default true,
    created_at timestamp default now(),

    fhir_metadata jsonb default '{}'
);


-- -- Enable RLS
-- alter table public.patients enable row level security;


-- -- Policies
-- create policy "Patients can read own data"
-- on public.patients
-- for select
-- using (auth.uid() = id);


-- -- Create policy for inserting patient data
-- create policy "Patients can insert own data"
-- on public.patients
-- for insert
-- with check (auth.uid() = id);


-- -- Create policy for updating patient data
-- create policy "Patients can update own data"
-- on public.patients
-- for update
-- using (auth.uid() = id);


-- -- Create policy for Patients to read own record
-- create policy "Patients can read own record"
-- on public.patients
-- for select
-- using (auth.uid() = id);


-- -- Create policy for Patients to insert own record (TEMP) in to the medical rec table
-- create policy "Patients can create own records (TEMP)"
-- on public.medical_records
-- for insert
-- with check (auth.uid() = patient_id);



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
