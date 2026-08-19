-- Assign the 'create_observation' permission to the 'doctor' role
insert into role_permissions (role_id, permission_id)
select r.id, p.id
from roles r, permissions p
where r.name = 'doctor'
and p.name = 'create_observation'
on conflict do nothing;
