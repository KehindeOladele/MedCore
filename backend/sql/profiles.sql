# ----- Create Profiles Table -----
create table if not exists public.profiles (
    id uuid primary key references auth.users(id) on delete cascade,
    email text,
    full_name text,
    role text default 'patient',
    created_at timestamp with time zone default timezone('utc', now())
);


# ----- Enable Row Level Security -----
alter table public.profiles enable row level security;


# ----- Create Policies -----
create policy "Users can read own profile"
on public.profiles
for select
using (auth.uid() = id);


# ---- Insert Policy -----
create policy "Users can insert own profile"
on public.profiles
for insert
with check (auth.uid() = id);
