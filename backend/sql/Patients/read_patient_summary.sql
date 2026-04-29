-- permission
insert into permissions (name)
values ('read_patient_summary');

-- assign to roles
insert into role_permissions (role_id, permission_id)
select r.id, p.id
from roles r, permissions p
where r.name in ('doctor', 'clinician')
and p.name = 'read_patient_summary';
