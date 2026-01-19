-- SQL script to create a roles table
create table roles (
    id uuid primary key default gen_random_uuid(),
    name text unique not null
);