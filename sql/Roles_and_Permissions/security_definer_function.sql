-- Security Definer (Helper Function)
create or replace function is_admin_user()
returns boolean
language sql
security definer
as $$
    select exists (
        select 1
        from user_roles ur
        join roles r on ur.role_id = r.id
        where ur.user_id = auth.uid()
        and r.name = 'admin'
    );
$$;