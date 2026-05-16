-- SQL script to create a permissions table
create table role_permissions (
    role_id uuid references roles(id) on delete cascade,
    permission_id uuid references permissions(id) on delete cascade,
    primary key (role_id, permission_id)
);