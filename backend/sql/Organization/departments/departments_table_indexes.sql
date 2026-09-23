-- Useful indexes: These will support the most common access patterns efficiently.
CREATE INDEX idx_departments_org
ON departments (organization_id);

CREATE INDEX idx_departments_parent
ON departments (parent_department_id);

CREATE INDEX idx_departments_active
ON departments (active);

CREATE INDEX idx_departments_deleted
ON departments (deleted_at);