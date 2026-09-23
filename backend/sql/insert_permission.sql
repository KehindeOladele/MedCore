-- Add permission to create observations
insert into permissions (name)
values ('create_observation')
on conflict do nothing;
