-- Doctors
insert into role_permissions
select r.id, p.id
from roles r, permissions p
where r.name = 'doctor'
and p.name in (
    'create_observation',
    'create_condition',
    'create_medication',
    'view_patient_record'
);

-- Clinicians
insert into role_permissions
select r.id, p.id
from roles r, permissions p
where r.name = 'clinician'
and p.name in (
    'create_observation',
    'create_condition',
    'view_patient_record'
);

-- Admin
insert into role_permissions
select r.id, p.id
from roles r, permissions p;
