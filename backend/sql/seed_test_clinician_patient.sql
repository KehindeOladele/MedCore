-- This SQL script inserts a record into the clinicians_patients table, associating a clinician with a patient. 
-- The clinician is identified by their user ID from the auth.users table, 
-- and the patient is identified by their ID from the patients table. 
-- The role of the clinician in relation to the patient is specified as 'primary', and the active status is set to true.
insert into clinicians_patients (
    clinician_id,
    patient_id,
    role,
    active
)
values (
    '892788c3-bd1f-42f6-8f51-5d5212324ae5', -- doctor (auth.users.id)
    'ac7bd263-8f96-4ef1-b0cf-8d245407d61f', -- patient.id
    'primary',
    true
);
