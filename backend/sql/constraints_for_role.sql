--  Check if roles table already has "name text unique".
-- select conname
-- from pg_constraint
-- where conrelid = 'roles'::regclass;

-- drop that old unique constraint first
-- alter table roles drop constraint roles_name_key;