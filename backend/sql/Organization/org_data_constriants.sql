-- Constraints to Improve data quality
ALTER TABLE organizations
ADD CONSTRAINT chk_website_length
CHECK (
    website IS NULL
    OR length(website) <= 255
);

ALTER TABLE organizations
ADD CONSTRAINT chk_timezone_length
CHECK (
    timezone IS NULL
    OR length(timezone) <= 100
);