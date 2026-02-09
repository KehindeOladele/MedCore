-- -- Table: clinicians
-- clinicians_patients
-- - clinician_id
-- - patient_id
-- - role (primary, consulting, emergency)
-- - active

--  Table to manage the many-to-many relationship between clinicians and patients, along with their roles and activity status.
create table clinicians_patients (
    clinician_id uuid references auth.users(id) on delete cascade,
    patient_id uuid references patients(id) on delete cascade,

    role text check (role in ('primary', 'consulting', 'emergency')) not null,
    active boolean default true,

    assigned_at timestamptz default now(),
    assigned_by uuid references auth.users(id),

    primary key (clinician_id, patient_id)
);


-- Indexes to optimize queries on the clinicians_patients table based on clinician_id and patient_id.
create index idx_clinicians_patients_patient
on clinicians_patients(patient_id);


-- Index to optimize queries on the clinicians_patients table based on clinician_id.
create index idx_clinicians_patients_clinician
on clinicians_patients(clinician_id);
