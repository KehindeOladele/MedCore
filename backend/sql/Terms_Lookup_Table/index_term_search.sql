-- ----- Index search for Terminology Codes -----
create index idx_terminology_search
on public.terminology_codes (system, display);