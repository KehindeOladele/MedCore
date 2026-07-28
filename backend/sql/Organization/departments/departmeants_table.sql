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