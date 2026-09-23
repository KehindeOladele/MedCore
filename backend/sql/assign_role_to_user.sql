-- Assign the 'doctor' role to the user with ID '892788c3-bd1f-42f6-8f51-5d5212324ae5'
insert into user_roles (user_id, role_id)
select
    '892788c3-bd1f-42f6-8f51-5d5212324ae5',
    r.id
from roles r
where r.name = 'doctor'
on conflict do nothing;
