<<<<<<< HEAD
-- Table for storing patient reminders
=======
-- Create the reminders table to store patient reminders and notifications.
>>>>>>> sql
create table if not exists public.reminders (
    id uuid primary key default gen_random_uuid(),

    patient_id uuid references patients(id),
    created_by uuid references auth.users(id),

    title text,
    description text,

    reminder_date timestamp,
    status text check (status in ('pending','done','missed')),

    created_at timestamp default now()
);
