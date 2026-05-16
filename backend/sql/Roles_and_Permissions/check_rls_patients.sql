-- Check if row-level security is enabled on the 'patients' table
select relrowsecurity
from pg_class
where relname = 'patients';
