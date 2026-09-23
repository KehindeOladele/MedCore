-- This allows different organizations to have a service named "Radiology", 
-- while preventing duplicate service names within the same organization.

ALTER TABLE healthcare_services
ADD CONSTRAINT healthcare_services_name_org_unique
UNIQUE (organization_id, name);