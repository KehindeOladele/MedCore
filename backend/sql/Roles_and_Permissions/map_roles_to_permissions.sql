-- Doctors
insert into role_permissions (role_id, permission_id)
select r.id, p.id
from roles r
join permissions p on p.name in (
    'create_observation',
    'create_condition',
    'create_medication',
    'view_patient_record'
)
where r.name = 'doctor'
on conflict do nothing;


-- Clinicians
insert into role_permissions (role_id, permission_id)
select r.id, p.id
from roles r
join permissions p on p.name in (
    'create_observation',
    'create_condition',
    'view_patient_record'
)
where r.name = 'clinician'
on conflict do nothing;

-- Admin
insert into role_permissions (role_id, permission_id)
select r.id, p.id
from roles r
cross join permissions p
where r.name = 'admin'
on conflict do nothing;
