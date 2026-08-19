-- These indexes support the most common query patterns for listing services 
-- by organization, department, availability, and clinical classification.

CREATE INDEX idx_healthcare_services_organization
ON healthcare_services (organization_id);

CREATE INDEX idx_healthcare_services_department
ON healthcare_services (department_id);

CREATE INDEX idx_healthcare_services_active
ON healthcare_services (active);

CREATE INDEX idx_healthcare_services_category
ON healthcare_services (category);

CREATE INDEX idx_healthcare_services_specialty
ON healthcare_services (specialty);