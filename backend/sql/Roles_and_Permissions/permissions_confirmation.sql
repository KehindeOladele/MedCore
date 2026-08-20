-- This query retrieves all roles that have been granted the 'resolve_condition' permission.
select
    r.name as role,
    p.name as permission
from role_permissions rp
join roles r on rp.role_id = r.id
join permissions p on rp.permission_id = p.id
where p.name = 'resolve_condition';
