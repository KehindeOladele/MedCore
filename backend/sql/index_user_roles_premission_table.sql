-- Indexes for user_roles and role_permissions tables
-- Your app will frequently query:
-- user roles by user_id
-- roles per organization
-- permissions per role

-- Indexes to optimize these queries
create index idx_user_roles_user on public.user_roles(user_id);
create index idx_user_roles_org on public.user_roles(organization_id);
create index idx_role_permissions_role on role_permissions(role_id);
create index idx_role_permissions_permission on role_permissions(permission_id);

-- Unique index to enforce unique role names within an organization
create unique index roles_unique_name_org
on roles (name, coalesce(organization_id, '00000000-0000-0000-0000-000000000000'));