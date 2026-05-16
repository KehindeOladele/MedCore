-- Insert new permission to resolve patient conditions
insert into permissions (name, description)
values (
    'resolve_condition',
    'Resolve an active patient condition'
);

-- insert new permissions for observations, conditions, patient QR codes, and FHIR bundles
insert into permissions (id, name, description)
values
    (gen_random_uuid(), 'create_observation', 'Create observation records'),
    (gen_random_uuid(), 'create_condition', 'Create condition records'),
    (gen_random_uuid(), 'view_patient_qr', 'View patient QR code'),
    (gen_random_uuid(), 'view_patient_fhir', 'View patient FHIR bundle');
