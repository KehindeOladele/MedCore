-- Create Healthcare Service table
-- | Column                      | Purpose                       | Future Use                         |
-- | --------------------------- | ----------------------------- | ---------------------------------- |
-- | `organization_id`           | Tenant boundary               | Required for every query           |
-- | `department_id`             | Organizes services            | Department → Healthcare Services   |
-- | `name`                      | Human-readable service name   | UI, scheduling, search             |
-- | `description`               | Patient-facing description    | Booking portal                     |
-- | `active`                    | Enable/disable service        | Soft retirement                    |
-- | `category`                  | High-level classification     | FHIR `HealthcareService.category`  |
-- | `type`                      | Service type                  | FHIR `HealthcareService.type`      |
-- | `specialty`                 | Clinical specialty            | FHIR `HealthcareService.specialty` |
-- | `appointment_required`      | Walk-in vs appointment        | Scheduling engine                  |
-- | `referral_required`         | Referral workflow             | Clinical business rules            |
-- | `online_booking_available`  | Self-service booking          | Patient portal                     |
-- | `phone`, `email`, `website` | Contact details               | FHIR `telecom` mapping             |
-- | `service_code`              | Internal or standardized code | Billing, interoperability          |
-- | `display_order`             | UI ordering                   | Setup Wizard and patient portal    |
-- | `deleted_at`                | Soft delete                   | Audit and recovery                 |
-- | `created_by`, `updated_by`  | Audit trail                   | Compliance                         |

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