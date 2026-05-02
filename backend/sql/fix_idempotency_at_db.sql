-- Fix Idempotency at DB Level
ALTER TABLE user_roles
ADD CONSTRAINT unique_user_role_org
UNIQUE (user_id, role_id, organization_id);