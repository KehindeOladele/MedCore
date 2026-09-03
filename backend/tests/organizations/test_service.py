import pytest
from datetime import datetime, timedelta
from types import SimpleNamespace

from app.modules.organizations import service
from app.modules.organizations.schemas import (
    OrganizationCreate,
    OrganizationUpdate,
    AcceptInviteRequest,
    RoleAssignment,
)
from tests.factories.constants import (
    ORGANIZATION_ID,
    USER_ID,
)


# ============================================================
# CREATE ORGANIZATION SERVICE
# ============================================================

def test_create_organization_success(
    mocker,
    organization_data,
):
    payload = OrganizationCreate(
        name=organization_data["name"],
        type=organization_data["type"],
        email=organization_data["email"],
        phone=organization_data["phone"],
        address=organization_data["address"],
        state=organization_data["state"],
        country=organization_data["country"],
        admin_email="admin@test.com",
        admin_password="password123",
    )

    admin_id = str(USER_ID)

    # ---------------------------------
    # Auth user creation
    # ---------------------------------
    auth_response = mocker.Mock()
    auth_response.user = SimpleNamespace(id=admin_id)

    auth = mocker.Mock()
    auth.admin.create_user.return_value = auth_response

    # ---------------------------------
    # Organization creation
    # ---------------------------------
    organization_response = mocker.Mock()
    organization_response.data = [organization_data]

    organization_query = mocker.Mock()
    organization_query.insert.return_value = organization_query
    organization_query.execute.return_value = organization_response

    # ---------------------------------
    # Default roles creation
    # ---------------------------------
    roles_insert_query = mocker.Mock()
    roles_insert_query.execute.return_value = mocker.Mock(
        data=[
            {"id": "role-admin"},
            {"id": "role-practitioner"},
            {"id": "role-staff"},
        ]
    )

    # ---------------------------------
    # org_admin role lookup
    # ---------------------------------
    role_response = mocker.Mock()
    role_response.data = {"id": "role-admin"}

    roles_lookup_query = mocker.Mock()
    roles_lookup_query.select.return_value = roles_lookup_query
    roles_lookup_query.eq.return_value = roles_lookup_query
    roles_lookup_query.single.return_value = roles_lookup_query
    roles_lookup_query.execute.return_value = role_response

    # ---------------------------------
    # User-role assignment
    # ---------------------------------
    user_role_query = mocker.Mock()
    user_role_query.insert.return_value = user_role_query
    user_role_query.execute.return_value = mocker.Mock(
        data=[
            {
                "user_id": admin_id,
                "role_id": "role-admin",
                "organization_id": organization_data["id"],
            }
        ]
    )

    # ---------------------------------
    # Roles table
    # ---------------------------------
    roles_table = mocker.Mock()
    roles_table.insert.return_value = roles_insert_query
    roles_table.select.return_value = roles_lookup_query

    # ---------------------------------
    # Supabase Admin
    # ---------------------------------
    supabase_admin = mocker.patch.object(
        service,
        "supabase_admin",
    )

    supabase_admin.auth = auth

    def table_side_effect(table_name):
        if table_name == "organizations":
            return organization_query

        if table_name == "roles":
            return roles_table

        if table_name == "user_roles":
            return user_role_query

        raise AssertionError(
            f"Unexpected table: {table_name}"
        )

    supabase_admin.table.side_effect = table_side_effect

    # ---------------------------------
    # Event
    # ---------------------------------
    emit_event = mocker.patch.object(
        service,
        "emit_event",
    )

    # ---------------------------------
    # Execute
    # ---------------------------------
    result = service.create_organization(payload)

    # ---------------------------------
    # Result
    # ---------------------------------
    assert result == {
        "message": "Organization registered successfully",
        "organization_id": organization_data["id"],
    }

    # ---------------------------------
    # Auth assertions
    # ---------------------------------
    auth.admin.create_user.assert_called_once_with({
        "email": "admin@test.com",
        "password": "password123",
        "email_confirm": True,
    })

    # ---------------------------------
    # Organization assertions
    # ---------------------------------
    organization_query.insert.assert_called_once_with(
        payload.model_dump(
            exclude={
                "admin_email",
                "admin_password",
            }
        )
    )

    # ---------------------------------
    # Default role assertions
    # ---------------------------------
    roles_table.insert.assert_called_once_with([
        {
            "name": "org_admin",
            "organization_id": organization_data["id"],
            "role_type": "organization",
        },
        {
            "name": "practitioner",
            "organization_id": organization_data["id"],
            "role_type": "organization",
        },
        {
            "name": "staff",
            "organization_id": organization_data["id"],
            "role_type": "organization",
        },
    ])

    # ---------------------------------
    # Role lookup assertions
    # ---------------------------------
    roles_table.select.assert_called_once_with("id")

    roles_lookup_query.eq.assert_any_call(
        "name",
        "org_admin",
    )

    roles_lookup_query.eq.assert_any_call(
        "organization_id",
        organization_data["id"],
    )

    # ---------------------------------
    # User-role assignment assertions
    # ---------------------------------
    user_role_query.insert.assert_called_once_with({
        "user_id": admin_id,
        "role_id": "role-admin",
        "organization_id": organization_data["id"],
    })

    # ---------------------------------
    # Event assertions
    # ---------------------------------
    emit_event.assert_called_once_with(
        aggregate_type="organization",
        aggregate_id=organization_data["id"],
        event_type=service.EventTypes.ORGANIZATION_CREATED,
        payload={
            "organization_id": organization_data["id"],
            "admin_user_id": admin_id,
            "organization_name": organization_data["name"],
            "admin_email": "admin@test.com",
        },
    )


def test_create_organization_raises_when_admin_user_creation_fails(
    mocker,
    organization_data,
):
    payload = OrganizationCreate(
        name=organization_data["name"],
        type=organization_data["type"],
        admin_email="admin@test.com",
        admin_password="password123",
    )

    auth_response = mocker.Mock()
    auth_response.user = None

    auth = mocker.Mock()
    auth.admin.create_user.return_value = auth_response

    supabase_admin = mocker.patch.object(
        service,
        "supabase_admin",
    )

    supabase_admin.auth = auth

    with pytest.raises(
        service.HTTPException,
        match="Failed to create admin user",
    ):
        service.create_organization(payload)

    auth.admin.create_user.assert_called_once()


def test_create_organization_raises_when_organization_creation_fails(
    mocker,
    organization_data,
):
    payload = OrganizationCreate(
        name=organization_data["name"],
        type=organization_data["type"],
        admin_email="admin@test.com",
        admin_password="password123",
    )

    auth_response = mocker.Mock()
    auth_response.user = SimpleNamespace(
        id=str(USER_ID)
    )

    auth = mocker.Mock()
    auth.admin.create_user.return_value = auth_response

    organization_response = mocker.Mock()
    organization_response.data = None

    organization_query = mocker.Mock()
    organization_query.insert.return_value = organization_query
    organization_query.execute.return_value = organization_response

    supabase_admin = mocker.patch.object(
        service,
        "supabase_admin",
    )

    supabase_admin.auth = auth
    supabase_admin.table.return_value = organization_query

    with pytest.raises(
        Exception,
        match="Failed to create organization",
    ):
        service.create_organization(payload)


def test_create_organization_raises_when_org_admin_role_not_found(
    mocker,
    organization_data,
):
    payload = OrganizationCreate(
        name=organization_data["name"],
        type=organization_data["type"],
        admin_email="admin@test.com",
        admin_password="password123",
    )

    auth_response = mocker.Mock()
    auth_response.user = SimpleNamespace(
        id=str(USER_ID)
    )

    auth = mocker.Mock()
    auth.admin.create_user.return_value = auth_response

    # ---------------------------------
    # Organization response
    # ---------------------------------
    organization_response = mocker.Mock()
    organization_response.data = [organization_data]

    organization_query = mocker.Mock()
    organization_query.insert.return_value = organization_query
    organization_query.execute.return_value = organization_response

    # ---------------------------------
    # Roles insert
    # ---------------------------------
    roles_insert_query = mocker.Mock()
    roles_insert_query.execute.return_value = mocker.Mock(
        data=[
            {"id": "role-1"},
            {"id": "role-2"},
            {"id": "role-3"},
        ]
    )

    # ---------------------------------
    # Role lookup fails
    # ---------------------------------
    role_response = mocker.Mock()
    role_response.data = None

    roles_lookup_query = mocker.Mock()
    roles_lookup_query.select.return_value = roles_lookup_query
    roles_lookup_query.eq.return_value = roles_lookup_query
    roles_lookup_query.single.return_value = roles_lookup_query
    roles_lookup_query.execute.return_value = role_response

    roles_table = mocker.Mock()
    roles_table.insert.return_value = roles_insert_query
    roles_table.select.return_value = roles_lookup_query

    supabase_admin = mocker.patch.object(
        service,
        "supabase_admin",
    )

    supabase_admin.auth = auth

    def table_side_effect(table_name):
        if table_name == "organizations":
            return organization_query

        if table_name == "roles":
            return roles_table

        raise AssertionError(
            f"Unexpected table: {table_name}"
        )

    supabase_admin.table.side_effect = table_side_effect

    with pytest.raises(
        Exception,
        match="org_admin role not found",
    ):
        service.create_organization(payload)


# ============================================================
# UPDATE ORGANIZATION SERVICE
# ============================================================

def test_update_organization_success(
    mocker,
    organization_data,
    updated_organization_data,
):
    payload = OrganizationUpdate(
        name="Updated Hospital",
    )

    response = mocker.Mock()
    response.data = [updated_organization_data]

    query = mocker.Mock()
    query.update.return_value = query
    query.eq.return_value = query
    query.execute.return_value = response

    supabase = mocker.patch.object(
        service,
        "supabase",
    )

    supabase.table.return_value = query

    result = service.update_organization(
        organization_data["id"],
        payload,
    )

    assert result == updated_organization_data

    supabase.table.assert_called_once_with(
        "organizations"
    )

    query.update.assert_called_once_with({
        "name": "Updated Hospital",
    })

    query.eq.assert_called_once_with(
        "id",
        organization_data["id"],
    )

    query.execute.assert_called_once_with()


def test_update_organization_raises_when_no_fields_provided(
    mocker,
    organization_data,
):
    payload = OrganizationUpdate()

    supabase = mocker.patch.object(
        service,
        "supabase",
    )

    with pytest.raises(
        service.HTTPException,
        match="No fields provided",
    ):
        service.update_organization(
            organization_data["id"],
            payload,
        )

    supabase.table.assert_not_called()


def test_update_organization_raises_when_organization_not_found(
    mocker,
    organization_data,
):
    payload = OrganizationUpdate(
        name="Updated Hospital",
    )

    response = mocker.Mock()
    response.data = None

    query = mocker.Mock()
    query.update.return_value = query
    query.eq.return_value = query
    query.execute.return_value = response

    supabase = mocker.patch.object(
        service,
        "supabase",
    )

    supabase.table.return_value = query

    with pytest.raises(
        service.HTTPException,
        match="Organization not found",
    ):
        service.update_organization(
            organization_data["id"],
            payload,
        )


# ============================================================
# ASSIGN USER ROLE SERVICE
# ============================================================

def test_assign_user_role_success(
    mocker,
    organization_data,
):
    role_data = RoleAssignment(
        user_id=USER_ID,
        role_name="practitioner",
        org_id=str(organization_data["id"]),
    )

    # ---------------------------------
    # Role lookup
    # ---------------------------------
    role_response = mocker.Mock()
    role_response.data = {
        "id": "role-practitioner"
    }

    role_query = mocker.Mock()
    role_query.select.return_value = role_query
    role_query.eq.return_value = role_query
    role_query.single.return_value = role_query
    role_query.execute.return_value = role_response

    # ---------------------------------
    # User-role mapping
    # ---------------------------------
    mapping = {
        "user_id": USER_ID,
        "role_id": "role-practitioner",
        "organization_id": organization_data["id"],
    }

    result_response = mocker.Mock()
    result_response.data = [mapping]

    user_role_query = mocker.Mock()
    user_role_query.upsert.return_value = user_role_query
    user_role_query.execute.return_value = result_response

    # ---------------------------------
    # Supabase
    # ---------------------------------
    supabase = mocker.patch.object(
        service,
        "supabase",
    )

    def table_side_effect(table_name):
        if table_name == "roles":
            return role_query

        if table_name == "user_roles":
            return user_role_query

        raise AssertionError(
            f"Unexpected table: {table_name}"
        )

    supabase.table.side_effect = table_side_effect

    # ---------------------------------
    # Execute
    # ---------------------------------
    result = service.assign_user_role(role_data)

    assert result == mapping

    role_query.select.assert_called_once_with("id")

    role_query.eq.assert_any_call(
        "name",
        "practitioner",
    )

    role_query.eq.assert_any_call(
        "organization_id",
        str(organization_data["id"]),
    )

    user_role_query.upsert.assert_called_once_with({
        "user_id": USER_ID,
        "role_id": "role-practitioner",
        "organization_id": str(organization_data["id"]),
    })


def test_assign_user_role_raises_when_role_not_found(
    mocker,
    organization_data,
):
    role_data = RoleAssignment(
        user_id=USER_ID,
        role_name="practitioner",
        org_id=str(organization_data["id"]),
    )

    role_response = mocker.Mock()
    role_response.data = None

    role_query = mocker.Mock()
    role_query.select.return_value = role_query
    role_query.eq.return_value = role_query
    role_query.single.return_value = role_query
    role_query.execute.return_value = role_response

    supabase = mocker.patch.object(
        service,
        "supabase",
    )

    supabase.table.return_value = role_query

    with pytest.raises(
        Exception,
        match="Role not found",
    ):
        service.assign_user_role(role_data)


def test_assign_user_role_raises_when_assignment_fails(
    mocker,
    organization_data,
):
    role_data = RoleAssignment(
        user_id=USER_ID,
        role_name="practitioner",
        org_id=str(organization_data["id"]),
    )

    role_response = mocker.Mock()
    role_response.data = {
        "id": "role-practitioner"
    }

    role_query = mocker.Mock()
    role_query.select.return_value = role_query
    role_query.eq.return_value = role_query
    role_query.single.return_value = role_query
    role_query.execute.return_value = role_response

    result_response = mocker.Mock()
    result_response.data = None

    user_role_query = mocker.Mock()
    user_role_query.upsert.return_value = user_role_query
    user_role_query.execute.return_value = result_response

    supabase = mocker.patch.object(
        service,
        "supabase",
    )

    def table_side_effect(table_name):
        if table_name == "roles":
            return role_query

        if table_name == "user_roles":
            return user_role_query

        raise AssertionError(
            f"Unexpected table: {table_name}"
        )

    supabase.table.side_effect = table_side_effect

    with pytest.raises(
        Exception,
        match="Failed to assign role",
    ):
        service.assign_user_role(role_data)


# ============================================================
# CREATE INVITATION SERVICE
# ============================================================

def test_create_invitation_success(
    mocker,
    organization_data,
):
    token = "test-invitation-token"

    mocker.patch.object(
        service.uuid,
        "uuid4",
        return_value=token,
    )

    invitation = {
        "id": "invite-1",
        "email": "staff@test.com",
        "organization_id": organization_data["id"],
        "role_name": "staff",
        "invited_by": USER_ID,
        "token": token,
    }

    response = mocker.Mock()
    response.data = [invitation]

    query = mocker.Mock()
    query.insert.return_value = query
    query.execute.return_value = response

    supabase = mocker.patch.object(
        service,
        "supabase",
    )

    supabase.table.return_value = query

    result = service.create_invitation(
        organization_data["id"],
        "staff@test.com",
        "staff",
        USER_ID,
    )

    assert result == invitation

    supabase.table.assert_called_once_with(
        "invitations"
    )

    query.insert.assert_called_once()

    inserted_data = query.insert.call_args.args[0]

    assert inserted_data["email"] == "staff@test.com"
    assert (
        inserted_data["organization_id"]
        == organization_data["id"]
    )
    assert inserted_data["role_name"] == "staff"
    assert inserted_data["invited_by"] == USER_ID
    assert inserted_data["token"] == token
    assert "expires_at" in inserted_data


def test_create_invitation_raises_when_insert_fails(
    mocker,
    organization_data,
):
    mocker.patch.object(
        service.uuid,
        "uuid4",
        return_value="test-token",
    )

    response = mocker.Mock()
    response.data = None

    query = mocker.Mock()
    query.insert.return_value = query
    query.execute.return_value = response

    supabase = mocker.patch.object(
        service,
        "supabase",
    )

    supabase.table.return_value = query

    with pytest.raises(
        Exception,
        match="Failed to create invitation",
    ):
        service.create_invitation(
            organization_data["id"],
            "staff@test.com",
            "staff",
            USER_ID,
        )


# ============================================================
# ACCEPT INVITATION SERVICE
# ============================================================

def test_accept_invitation_success(
    mocker,
    organization_data,
):
    token = "test-token"
    user_id = str(USER_ID)

    payload = AcceptInviteRequest(
        token=token,
        password="password123",
    )

    invitation = {
        "id": "invite-1",
        "email": "staff@test.com",
        "organization_id": str(organization_data["id"]),
        "role_name": "staff",
        "expires_at": (
            datetime.now() + timedelta(days=1)
        ).isoformat(),
        "status": "pending",
    }

    # ---------------------------------
    # Invitation lookup
    # ---------------------------------
    invitation_response = mocker.Mock()
    invitation_response.data = invitation

    invitation_query = mocker.Mock()
    invitation_query.select.return_value = invitation_query
    invitation_query.eq.return_value = invitation_query
    invitation_query.single.return_value = invitation_query
    invitation_query.execute.return_value = invitation_response
    invitation_query.update.return_value = invitation_query

    # ---------------------------------
    # Auth signup
    # ---------------------------------
    auth_response = mocker.Mock()
    auth_response.user = SimpleNamespace(
        id=user_id
    )

    auth = mocker.Mock()
    auth.sign_up.return_value = auth_response

    # ---------------------------------
    # Role lookup
    # ---------------------------------
    role_response = mocker.Mock()
    role_response.data = {
        "id": "role-staff"
    }

    role_query = mocker.Mock()
    role_query.select.return_value = role_query
    role_query.eq.return_value = role_query
    role_query.single.return_value = role_query
    role_query.execute.return_value = role_response

    # ---------------------------------
    # User-role assignment
    # ---------------------------------
    user_role_query = mocker.Mock()
    user_role_query.insert.return_value = user_role_query
    user_role_query.execute.return_value = mocker.Mock(
        data=[
            {
                "user_id": user_id,
                "role_id": "role-staff",
                "organization_id": str(organization_data["id"]),
            }
        ]
    )

    # ---------------------------------
    # Invitation update
    # ---------------------------------
    invitation_update_query = mocker.Mock()
    invitation_update_query.update.return_value = (
        invitation_update_query
    )
    invitation_update_query.eq.return_value = (
        invitation_update_query
    )
    invitation_update_query.execute.return_value = mocker.Mock(
        data=[
            {
                "id": "invite-1",
                "status": "accepted",
            }
        ]
    )

    # ---------------------------------
    # Supabase
    # ---------------------------------
    supabase = mocker.patch.object(
        service,
        "supabase",
    )

    supabase.auth = auth

    def table_side_effect(table_name):
        if table_name == "invitations":
            return invitation_query

        if table_name == "roles":
            return role_query

        if table_name == "user_roles":
            return user_role_query

        raise AssertionError(
            f"Unexpected table: {table_name}"
        )

    supabase.table.side_effect = table_side_effect

    # ---------------------------------
    # Execute
    # ---------------------------------
    result = service.accept_invitation(payload)

    assert result == {
        "message": "Account created successfully",
        "user_id": user_id,
    }

    # ---------------------------------
    # Invitation lookup
    # ---------------------------------
    invitation_query.select.assert_called_once_with("*")

    invitation_query.eq.assert_any_call(
        "token",
        token,
    )

    invitation_query.eq.assert_any_call(
        "status",
        "pending",
    )

    # ---------------------------------
    # Auth signup
    # ---------------------------------
    auth.sign_up.assert_called_once_with({
        "email": "staff@test.com",
        "password": "password123",
    })

    # ---------------------------------
    # Role lookup
    # ---------------------------------
    role_query.select.assert_called_once_with("id")

    role_query.eq.assert_any_call(
        "name",
        "staff",
    )

    role_query.eq.assert_any_call(
        "organization_id",
        str(organization_data["id"]),
    )

    # ---------------------------------
    # User-role assignment
    # ---------------------------------
    user_role_query.insert.assert_called_once_with({
        "user_id": user_id,
        "role_id": "role-staff",
        "organization_id": str(organization_data["id"]),
    })


def test_accept_invitation_raises_when_invitation_is_invalid(
    mocker,
):
    payload = AcceptInviteRequest(
        token="invalid-token",
        password="password123",
    )

    invitation_response = mocker.Mock()
    invitation_response.data = None

    invitation_query = mocker.Mock()
    invitation_query.select.return_value = invitation_query
    invitation_query.eq.return_value = invitation_query
    invitation_query.single.return_value = invitation_query
    invitation_query.execute.return_value = invitation_response

    supabase = mocker.patch.object(
        service,
        "supabase",
    )

    supabase.table.return_value = invitation_query

    with pytest.raises(
        Exception,
        match="Invalid or expired invitation",
    ):
        service.accept_invitation(payload)


def test_accept_invitation_raises_when_invitation_expired(
    mocker,
    organization_data,
):
    payload = AcceptInviteRequest(
        token="expired-token",
        password="password123",
    )

    invitation = {
        "id": "invite-1",
        "email": "staff@test.com",
        "organization_id": organization_data["id"],
        "role_name": "staff",
        "expires_at": (
            datetime.now() - timedelta(days=1)
        ).isoformat(),
        "status": "pending",
    }

    invitation_response = mocker.Mock()
    invitation_response.data = invitation

    invitation_query = mocker.Mock()
    invitation_query.select.return_value = invitation_query
    invitation_query.eq.return_value = invitation_query
    invitation_query.single.return_value = invitation_query
    invitation_query.execute.return_value = invitation_response

    supabase = mocker.patch.object(
        service,
        "supabase",
    )

    supabase.table.return_value = invitation_query

    with pytest.raises(
        Exception,
        match="Invitation expired",
    ):
        service.accept_invitation(payload)


def test_accept_invitation_raises_when_signup_fails(
    mocker,
    organization_data,
):
    payload = AcceptInviteRequest(
        token="test-token",
        password="password123",
    )

    invitation = {
        "id": "invite-1",
        "email": "staff@test.com",
        "organization_id": organization_data["id"],
        "role_name": "staff",
        "expires_at": (
            datetime.now() + timedelta(days=1)
        ).isoformat(),
        "status": "pending",
    }

    invitation_response = mocker.Mock()
    invitation_response.data = invitation

    invitation_query = mocker.Mock()
    invitation_query.select.return_value = invitation_query
    invitation_query.eq.return_value = invitation_query
    invitation_query.single.return_value = invitation_query
    invitation_query.execute.return_value = invitation_response

    auth_response = mocker.Mock()
    auth_response.user = None

    auth = mocker.Mock()
    auth.sign_up.return_value = auth_response

    supabase = mocker.patch.object(
        service,
        "supabase",
    )

    supabase.table.return_value = invitation_query
    supabase.auth = auth

    with pytest.raises(
        Exception,
        match="Signup failed",
    ):
        service.accept_invitation(payload)


def test_accept_invitation_raises_when_role_not_found(
    mocker,
    organization_data,
):
    payload = AcceptInviteRequest(
        token="test-token",
        password="password123",
    )

    invitation = {
        "id": "invite-1",
        "email": "staff@test.com",
        "organization_id": organization_data["id"],
        "role_name": "staff",
        "expires_at": (
            datetime.now() + timedelta(days=1)
        ).isoformat(),
        "status": "pending",
    }

    invitation_response = mocker.Mock()
    invitation_response.data = invitation

    invitation_query = mocker.Mock()
    invitation_query.select.return_value = invitation_query
    invitation_query.eq.return_value = invitation_query
    invitation_query.single.return_value = invitation_query
    invitation_query.execute.return_value = invitation_response

    auth_response = mocker.Mock()
    auth_response.user = SimpleNamespace(
        id=str(USER_ID)
    )

    auth = mocker.Mock()
    auth.sign_up.return_value = auth_response

    role_response = mocker.Mock()
    role_response.data = None

    role_query = mocker.Mock()
    role_query.select.return_value = role_query
    role_query.eq.return_value = role_query
    role_query.single.return_value = role_query
    role_query.execute.return_value = role_response

    supabase = mocker.patch.object(
        service,
        "supabase"
    )

    supabase.auth = auth

    def table_side_effect(table_name):
        if table_name == "invitations":
            return invitation_query

        if table_name == "roles":
            return role_query

        raise AssertionError(
            f"Unexpected table: {table_name}"
        )

    supabase.table.side_effect = table_side_effect

    with pytest.raises(
        Exception,
        match="Role not found",
    ):
        service.accept_invitation(payload)