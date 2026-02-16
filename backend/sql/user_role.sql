-- Mapping table to associate users with roles
create table if not exists public.user_roles (
    user_id uuid references auth.users(id) on delete cascade,
    role_id uuid references public.roles(id) on delete cascade,
    assigned_at timestamptz default now(),
    primary key (user_id, role_id)
);


-- Enable row level security for user_roles table
alter table public.user_roles enable row level security;


-- Policy to allow users to read their own roles
create policy "Users read own roles"
on public.user_roles
for select
using (auth.uid() = user_id);



-- Policy to allow admins to manage roles
create policy "Admins manage roles"
on public.user_roles
for all
using (
    exists (
    select 1 from user_roles ur
    join roles r on ur.role_id = r.id
    where ur.user_id = auth.uid()
    and r.name = 'admin'
    )
);
