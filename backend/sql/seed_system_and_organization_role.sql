-- ----- Create Patient and organizations system in Roles -----
-- SYSTEM ROLES (global)
insert into roles (name, role_type) values
('patient', 'system'),
('super_admin', 'system')
on conflict do nothing;


-- ----- ORGANIZATION ROLES -----
-- insert into roles (name, role_type, organization_id) values
-- ('org_admin', 'organization', '<ORG_ID>'),
-- ('practitioner', 'organization', '<ORG_ID>'),
-- ('staff', 'organization', '<ORG_ID>');