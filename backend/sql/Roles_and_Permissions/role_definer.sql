-- Function to retrieve all permissions for a given user based on their roles
create or replace function get_user_permissions(uid uuid)
returns table(permission text)
language sql
security definer
as $$
    select p.name
    from user_roles ur
    join role_permissions rp on ur.role_id = rp.role_id
    join permissions p on rp.permission_id = p.id
    where ur.user_id = uid;
$$;
