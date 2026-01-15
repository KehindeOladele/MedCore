-- Create Terminology Codes Lookup Table
create table if not exists public.terminology_codes (
    id uuid default gen_random_uuid() primary key,
    system text not null, -- SNOMED | LOINC | RxNorm
    code text not null,
    display text not null
);

-- Create indexes for faster lookups (system)
create index on public.terminology_codes (system);

-- Create indexes for faster lookups (code)
create index on public.terminology_codes (code);
