-- Create Department Table
-- organization_id: Supports multi-tenancy, queries are scope by organization_id.
-- parent_department_id: Supports departmental hierarchy.
-- code: 
-- Codes are often used in:
    -- Billing
    -- HL7 integrations
    -- Reporting
    -- Internal APIs
-- active: Avoids deleting departments that have practitioners or historical records.
-- Audit Fields: That keeps every business module consistent.
    -- created_by
    -- updated_by
    -- created_at
    -- updated_at
    -- deleted_at
CREATE TABLE departments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    organization_id UUID NOT NULL
        REFERENCES organizations(id)
        ON DELETE CASCADE,

    parent_department_id UUID NULL
        REFERENCES departments(id)
        ON DELETE SET NULL,

    name TEXT NOT NULL,

    code TEXT,

    description TEXT,

    active BOOLEAN NOT NULL DEFAULT TRUE,

    created_by UUID REFERENCES auth.users(id),

    updated_by UUID REFERENCES auth.users(id),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    deleted_at TIMESTAMPTZ
);



-- Supabase RLS 
ALTER TABLE departments
ENABLE ROW LEVEL SECURITY;