-- This query retrieves all roles along with their associated permissions.
select
    r.name as role,
    p.name as permission
from role_permissions rp
join roles r on r.id = rp.role_id
join permissions p on p.id = rp.permission_id
order by r.name, p.name;
