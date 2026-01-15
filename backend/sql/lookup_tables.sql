create table if not exists public.terminology_codes (
    id uuid default gen_random_uuid() primary key,
    system text not null, -- SNOMED | LOINC | RxNorm
    code text not null,
    display text not null
);

create index on public.terminology_codes (system);
create index on public.terminology_codes (code);
