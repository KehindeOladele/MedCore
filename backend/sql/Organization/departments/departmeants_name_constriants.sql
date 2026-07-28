-- Unique Hospitatl Name and Access constriants
-- This allows:
    -- Hospital A
    --     Cardiology

    -- Hospital B
    --     Cardiology
-- while preventing:
    -- Hospital A

    -- Cardiology
    -- Cardiology
ALTER TABLE departments
ADD CONSTRAINT unique_department_name_per_organization
UNIQUE (organization_id, name);