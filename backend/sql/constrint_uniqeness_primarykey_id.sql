-- -- Add Primary key id to user_roles table
-- alter table user_roles
-- add column id uuid primary key default gen_random_uuid();


-- -- Enforcing uniqueness in user_roles table
-- alter table user_roles
-- add constraint unique_user_role_org
-- unique (user_id, role_id, organization_id);

-- 1) Add the column only if it doesn't exist
-- ALTER TABLE user_roles
-- ADD COLUMN IF NOT EXISTS id uuid DEFAULT gen_random_uuid();

-- 2) Add primary key only if it doesn't exist
-- DO $$
-- BEGIN
--   IF NOT EXISTS (
--     SELECT 1
--     FROM pg_constraint
--     WHERE conname = 'user_roles_pkey'
--   ) THEN
--     ALTER TABLE user_roles
--     ADD CONSTRAINT user_roles_pkey PRIMARY KEY (id);
--   END IF;
-- END $$;



-- Insert policy for user_roles
-- Allow inserts for authenticated users (basic version)
-- create policy "Allow insert for authenticated users"
-- on user_roles
-- for insert
-- to authenticated
-- with check (true);

-- create policy "Allow service role full access"
-- on user_roles
-- for all
-- to service_role
-- using (true)
-- with check (true);


--  Users can only assign to themselves
create policy "Users can only assign roles to themselves"
on user_roles
for insert
to authenticated
with check (auth.uid() = user_id);