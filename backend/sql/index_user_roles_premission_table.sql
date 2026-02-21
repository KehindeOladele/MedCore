-- Indexes for user_roles and role_permissions tables
create index idx_user_roles_user on public.user_roles(user_id);
create index idx_user_roles_org on public.user_roles(organization_id);
create index idx_role_permissions_role on role_permissions(role_id);
create index idx_role_permissions_permission on role_permissions(permission_id);