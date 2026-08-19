-- This query grants the 'resolve_condition' permission to the 'clinician' role.
insert into role_permissions (role_id, permission_id)
select
    r.id,
    p.id
from roles r, permissions p
where r.name = 'clinician'
    and p.name = 'resolve_condition';