-- Table to manage care teams for patients
create table care_teams (
    id uuid primary key default gen_random_uuid(),
    patient_id uuid not null references patients(id) on delete cascade,
    clinician_id uuid not null references clinicians(id) on delete cascade,
    role text not null default 'primary', -- primary | consultant | nurse | emergency
    assigned_at timestamptz default now(),
    unique (patient_id, clinician_id)
);
