-- SQL script to create a role permissions table
create table permissions (
    id uuid primary key default gen_random_uuid(),
    name text unique not null,
    description text
);
