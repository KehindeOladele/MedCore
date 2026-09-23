-- Add state country and logo_url to organizations table
alter table organizations add column if not exists state text;
alter table organizations add column if not exists country text;
alter table organizations add column if not exists logo_url text;