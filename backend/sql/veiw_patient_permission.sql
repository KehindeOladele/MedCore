-- Insert the view_patient permission
insert into permissions (name)
values ('view_patient')
on conflict do nothing;


-- Assign the view_patient permission to doctor, clinician, and patient roles
insert into role_permissions (role_id, permission_id)
select r.id, p.id
from roles r
join permissions p on p.name = 'view_patient'
where r.name in ('doctor', 'clinician', 'patient')
on conflict do nothing;
