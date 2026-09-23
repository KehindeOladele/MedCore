-- permissions organization
insert into permissions (name) values
('manage_organization'),
('invite_user'),
('assign_role'),
('view_patient'),
('assign_patient')
ON CONFLICT (name) DO NOTHING;

-- role_permissions mapping organizations
-- org_admin gets everything
insert into role_permissions (role_id, permission_id)
select r.id, p.id
from roles r, permissions p
where r.name = 'org_admin';

-- practitioner
insert into role_permissions (role_id, permission_id)
select r.id, p.id
from roles r
join permissions p on p.name in ('view_patient')
where r.name = 'practitioner';

-- staff
insert into role_permissions (role_id, permission_id)
select r.id, p.id
from roles r
join permissions p on p.name in ('view_patient')
where r.name = 'staff';