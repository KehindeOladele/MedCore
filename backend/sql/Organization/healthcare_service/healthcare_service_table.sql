-- Create Healthcare Service table


CREATE TABLE healthcare_services (
    -- Primary Key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Multi-tenancy
    organization_id UUID NOT NULL
        REFERENCES organizations(id)
        ON DELETE CASCADE,

    -- Organizational grouping
    department_id UUID
        REFERENCES departments(id)
        ON DELETE SET NULL,

    -- Core Service Information
    name TEXT NOT NULL,
    description TEXT,

    active BOOLEAN NOT NULL DEFAULT TRUE,

    -- FHIR Classification
    category TEXT,
    type TEXT,
    specialty TEXT,

    -- Patient Access
    appointment_required BOOLEAN NOT NULL DEFAULT TRUE,
    referral_required BOOLEAN NOT NULL DEFAULT FALSE,
    online_booking_available BOOLEAN NOT NULL DEFAULT FALSE,

    -- Contact Information
    phone TEXT,
    email TEXT,
    website TEXT,

    -- Operational Metadata
    service_code TEXT,
    display_order INTEGER DEFAULT 0,

    -- Lifecycle
    deleted_at TIMESTAMPTZ,

    -- Audit
    created_by UUID,
    updated_by UUID,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);