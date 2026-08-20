-- Branding is organization identity, so it stays on the organizations table.
-- logo_path is internal storage metadata; clients receive only logo_url.
ALTER TABLE organizations
    ADD COLUMN IF NOT EXISTS logo_path TEXT,
    ADD COLUMN IF NOT EXISTS primary_color VARCHAR(7),
    ADD COLUMN IF NOT EXISTS secondary_color VARCHAR(7);

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'organizations_primary_color_hex'
    ) THEN
        ALTER TABLE organizations ADD CONSTRAINT organizations_primary_color_hex CHECK (
            primary_color IS NULL OR primary_color ~ '^#[0-9A-Fa-f]{6}$'
        );
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'organizations_secondary_color_hex'
    ) THEN
        ALTER TABLE organizations ADD CONSTRAINT organizations_secondary_color_hex CHECK (
            secondary_color IS NULL OR secondary_color ~ '^#[0-9A-Fa-f]{6}$'
        );
    END IF;
END $$;
