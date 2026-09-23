-- Weekly organization hours for the Organization Setup Wizard.
-- Multiple rows per weekday permit split shifts; soft deletion retains audit history.
CREATE TABLE organization_operating_hours (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    day_of_week SMALLINT NOT NULL CHECK (day_of_week BETWEEN 0 AND 6),
    slot_index SMALLINT NOT NULL DEFAULT 0 CHECK (slot_index >= 0),
    opens_at TIME,
    closes_at TIME,
    is_closed BOOLEAN NOT NULL DEFAULT FALSE,
    created_by UUID,
    updated_by UUID,
    deleted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT operating_hours_time_shape CHECK (
        (is_closed AND opens_at IS NULL AND closes_at IS NULL)
        OR
        (NOT is_closed AND opens_at IS NOT NULL AND closes_at IS NOT NULL AND opens_at < closes_at)
    ),
    CONSTRAINT operating_hours_slot_unique UNIQUE (organization_id, day_of_week, slot_index)
);

CREATE INDEX organization_operating_hours_lookup_idx
ON organization_operating_hours (organization_id, day_of_week, slot_index)
WHERE deleted_at IS NULL;
