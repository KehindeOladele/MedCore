from unittest.mock import Mock

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from main import app

from app.core.security import get_current_user
from app.modules.organizations import router
from app.modules.organizations.exceptions import (
    OrganizationNotFoundError,
    UserOrganizationNotFoundError,
)

from tests.factories.constants import (
    ORGANIZATION_ID,
    USER_ID,
)


# ============================================================
# TEST DATA
# ============================================================


REGISTER_PAYLOAD = {
    "name": "Test Hospital",
    "type": "hospital",
    "email": "admin@test.com",
    "phone": "08012345678",
    "address": "123 Main Street",
    "state": "Lagos",
    "country": "Nigeria",
    "admin_email": "admin@test.com",
    "admin_password": "SecurePassword123!",
}


UPDATE_PAYLOAD = {
    "name": "Updated Hospital",
    "type": "hospital",
    "email": "updated@test.com",
    "phone": "08098765432",
    "address": "456 New Street",
    "state": "Abuja",
    "country": "Nigeria",
}


ROLE_PAYLOAD = {
    "user_id": str(USER_ID),
    "role_name": "practitioner",
    "org_id": str(ORGANIZATION_ID),
}


INVITE_PAYLOAD = {
    "email": "staff@test.com",
    "role_name": "staff",
    "org_id": str(ORGANIZATION_ID),
}


ACCEPT_INVITE_PAYLOAD = {
    "token": "test-invitation-token",
    "password": "SecurePassword123!",
}


# ============================================================
# HELPERS
# ============================================================


def _find_manage_organization_dependency():
    """
    Locate the already-registered dependency produced by:

        require_permission("manage_organization")

    The permission dependency is a closure, so calling
    require_permission() again would create a different callable
    and would not override the dependency already registered
    on the route.
    """

    for route in app.routes:
        dependant = getattr(route, "dependant", None)

        if dependant is None:
            continue

        for dependency in dependant.dependencies:
            call = dependency.call

            if call is None:
                continue

            closure = getattr(call, "__closure__", None)

            if not closure:
                continue

            for cell in closure:
                try:
                    value = cell.cell_contents
                except ValueError:
                    continue

                if value == "manage_organization":
                    return call

    raise AssertionError(
        "Could not find the registered "
        "require_permission('manage_organization') dependency."
    )


def _override_manage_organization_permission(
    dependency_override,
):
    """
    Override the exact dependency callable registered by
    the Organization router.
    """

    permission_dependency = _find_manage_organization_dependency()

    app.dependency_overrides[
        permission_dependency
    ] = dependency_override


# ============================================================
# ORGANIZATION REGISTRATION
# ============================================================


def test_register_organization_success(
    client,
    mocker,
):
    create_organization = mocker.patch.object(
        router,
        "create_organization",
        return_value={
            "message": "Organization registered successfully",
            "organization_id": str(ORGANIZATION_ID),
        },
    )

    response = client.post(
        "/organizations/register",
        json=REGISTER_PAYLOAD,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == (
        "Organization registered successfully"
    )
    assert body["organization_id"] == str(ORGANIZATION_ID)

    create_organization.assert_called_once()

    payload = create_organization.call_args.args[0]

    assert payload.name == REGISTER_PAYLOAD["name"]
    assert payload.type == REGISTER_PAYLOAD["type"]
    assert payload.email == REGISTER_PAYLOAD["email"]
    assert payload.admin_email == REGISTER_PAYLOAD["admin_email"]
    assert (
        payload.admin_password
        == REGISTER_PAYLOAD["admin_password"]
    )


def test_register_organization_invalid_payload(
    client,
):
    response = client.post(
        "/organizations/register",
        json={
            "name": "Test Hospital",
            "type": "hospital",
            "email": "not-an-email",
            "admin_email": "admin@test.com",
            "admin_password": "SecurePassword123!",
        },
    )

    assert response.status_code == 422


def test_register_organization_service_exception_propagates(
    client,
    mocker,
):
    mocker.patch.object(
        router,
        "create_organization",
        side_effect=HTTPException(
            status_code=400,
            detail="Failed to create admin user",
        ),
    )

    response = client.post(
        "/organizations/register",
        json=REGISTER_PAYLOAD,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Failed to create admin user"
    )


# ============================================================
# GET MY ORGANIZATION
# ============================================================


def test_get_my_organization_success(
    authenticated_client,
    mocker,
    organization_data,
):
    get_org_id = mocker.patch.object(
        router,
        "get_user_organization_id",
        return_value=str(ORGANIZATION_ID),
    )

    get_org = mocker.patch.object(
        router,
        "get_organization",
        return_value=organization_data,
    )

    response = authenticated_client.get(
        "/organizations/me"
    )

    assert response.status_code == 200
    assert response.json() == organization_data

    get_org_id.assert_called_once_with(
        str(USER_ID)
    )

    get_org.assert_called_once_with(
        str(ORGANIZATION_ID)
    )


def test_get_my_organization_user_has_no_organization(
    authenticated_client,
    mocker,
):
    mocker.patch.object(
        router,
        "get_user_organization_id",
        side_effect=UserOrganizationNotFoundError(
            "User is not assigned to an organization."
        ),
    )

    response = authenticated_client.get(
        "/organizations/me"
    )

    assert response.status_code == 404


def test_get_my_organization_not_found(
    authenticated_client,
    mocker,
):
    mocker.patch.object(
        router,
        "get_user_organization_id",
        return_value=str(ORGANIZATION_ID),
    )

    mocker.patch.object(
        router,
        "get_organization",
        side_effect=OrganizationNotFoundError(
            "Organization not found."
        ),
    )

    response = authenticated_client.get(
        "/organizations/me"
    )

    assert response.status_code == 404


# ============================================================
# UPLOAD ORGANIZATION LOGO
# ============================================================


def test_upload_organization_logo_success(
    authenticated_client,
    mocker,
):
    get_org_id = mocker.patch.object(
        router,
        "get_user_organization_id",
        return_value=str(ORGANIZATION_ID),
    )

    public_url = (
        "https://storage.test/organization-logos/"
        f"{ORGANIZATION_ID}.png"
    )

    bucket = Mock()

    bucket.upload.return_value = {
        "path": f"{ORGANIZATION_ID}.png"
    }

    bucket.get_public_url.return_value = public_url

    storage = Mock()
    storage.from_.return_value = bucket

    supabase = mocker.patch.object(
        router,
        "supabase",
    )

    supabase.storage = storage

    organizations_query = Mock()

    organizations_query.update.return_value = (
        organizations_query
    )
    organizations_query.eq.return_value = (
        organizations_query
    )
    organizations_query.execute.return_value = Mock(
        data=[
            {
                "id": str(ORGANIZATION_ID),
                "logo_url": public_url,
            }
        ]
    )

    supabase.table.return_value = organizations_query

    content = b"\x89PNG\r\n\x1a\nfake-png"

    response = authenticated_client.post(
        "/organizations/upload-logo",
        files={
            "file": (
                "logo.png",
                content,
                "image/png",
            )
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == (
        "Logo uploaded successfully"
    )
    assert body["logo_url"] == public_url

    get_org_id.assert_called_once_with()

    storage.from_.assert_called_once_with(
        "organization-logos"
    )

    bucket.upload.assert_called_once_with(
        path=f"{ORGANIZATION_ID}.png",
        file=content,
        file_options={
            "content-type": "image/png",
        },
    )

    bucket.get_public_url.assert_called_once_with(
        f"{ORGANIZATION_ID}.png"
    )

    organizations_query.update.assert_called_once_with(
        {
            "logo_url": public_url,
        }
    )

    organizations_query.eq.assert_called_once_with(
        "id",
        str(ORGANIZATION_ID),
    )

    organizations_query.execute.assert_called_once()


def test_upload_organization_logo_requires_authentication(
    client,
):
    response = client.post(
        "/organizations/upload-logo",
        files={
            "file": (
                "logo.png",
                b"fake",
                "image/png",
            )
        },
    )

    assert response.status_code == 401


# ============================================================
# UPDATE ORGANIZATION
# ============================================================


def test_update_my_organization_success(
    authenticated_client,
    mocker,
    updated_organization_data,
):
    mock_get_org_id = mocker.patch.object(
        router,
        "get_user_organization_id",
        return_value=str(ORGANIZATION_ID),
    )

    mock_update = mocker.patch.object(
        router,
        "update_organization",
        return_value=updated_organization_data,
    )

    permission_override = Mock(
        return_value={
            "id": str(ORGANIZATION_ID),
            "name": "Test Hospital",
        }
    )

    _override_manage_organization_permission(
        permission_override
    )

    response = authenticated_client.put(
        "/organizations/update",
        json=UPDATE_PAYLOAD,
    )

    assert response.status_code == 200
    assert response.json() == updated_organization_data

    mock_get_org_id.assert_called_once_with(
        str(USER_ID)
    )

    mock_update.assert_called_once()

    call_args = mock_update.call_args

    assert call_args.args[0] == str(ORGANIZATION_ID)

    payload = call_args.args[1]

    assert payload.name == UPDATE_PAYLOAD["name"]
    assert payload.email == UPDATE_PAYLOAD["email"]
    assert payload.phone == UPDATE_PAYLOAD["phone"]


def test_update_my_organization_invalid_payload(
    authenticated_client,
    mocker,
):
    permission_override = Mock(
        return_value={
            "id": str(ORGANIZATION_ID),
            "name": "Test Hospital",
        }
    )

    _override_manage_organization_permission(
        permission_override
    )

    response = authenticated_client.put(
        "/organizations/update",
        json={
            "email": "not-an-email",
        },
    )

    assert response.status_code == 422


def test_update_my_organization_permission_denied(
    authenticated_client,
    mocker,
):
    permission_override = Mock(
        side_effect=HTTPException(
            status_code=403,
            detail="Permission denied",
        )
    )

    _override_manage_organization_permission(
        permission_override
    )

    response = authenticated_client.put(
        "/organizations/update",
        json=UPDATE_PAYLOAD,
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "Permission denied"
    )


def test_update_my_organization_service_exception_propagates(
    authenticated_client,
    mocker,
):
    permission_override = Mock(
        return_value={
            "id": str(ORGANIZATION_ID),
            "name": "Test Hospital",
        }
    )

    _override_manage_organization_permission(
        permission_override
    )

    mocker.patch.object(
        router,
        "get_user_organization_id",
        return_value=str(ORGANIZATION_ID),
    )

    mocker.patch.object(
        router,
        "update_organization",
        side_effect=HTTPException(
            status_code=404,
            detail="Organization not found",
        ),
    )

    response = authenticated_client.put(
        "/organizations/update",
        json=UPDATE_PAYLOAD,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Organization not found"
    )


# ============================================================
# ASSIGN USER ROLE
# ============================================================


def test_assign_role_success(
    authenticated_client,
    mocker,
):
    permission_override = Mock(
        return_value={
            "id": str(ORGANIZATION_ID),
            "name": "Test Hospital",
        }
    )

    _override_manage_organization_permission(
        permission_override
    )

    assign_role = mocker.patch.object(
        router,
        "assign_user_role",
        return_value={
            "id": "user-role-1",
            "user_id": str(USER_ID),
            "role_id": "role-1",
            "organization_id": str(ORGANIZATION_ID),
        },
    )

    response = authenticated_client.post(
        f"/organizations/{ORGANIZATION_ID}/assign-role",
        json=ROLE_PAYLOAD,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["user_id"] == str(USER_ID)
    assert body["organization_id"] == str(ORGANIZATION_ID)

    assign_role.assert_called_once_with(
        {
            "user_id": USER_ID,
            "role_name": "practitioner",
            "org_id": str(ORGANIZATION_ID),
        }
    )


def test_assign_role_organization_mismatch(
    authenticated_client,
    mocker,
):
    permission_override = Mock(
        return_value={
            "id": str(ORGANIZATION_ID),
            "name": "Test Hospital",
        }
    )

    _override_manage_organization_permission(
        permission_override
    )

    assign_role = mocker.patch.object(
        router,
        "assign_user_role",
    )

    response = authenticated_client.post(
        f"/organizations/{ORGANIZATION_ID}/assign-role",
        json={
            "user_id": str(USER_ID),
            "role_name": "practitioner",
            "org_id": "22222222-2222-2222-2222-222222222222",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Organization mismatch"
    )

    assign_role.assert_not_called()


def test_assign_role_permission_denied(
    authenticated_client,
    mocker,
):
    permission_override = Mock(
        side_effect=HTTPException(
            status_code=403,
            detail="Permission denied",
        )
    )

    _override_manage_organization_permission(
        permission_override
    )

    assign_role = mocker.patch.object(
        router,
        "assign_user_role",
    )

    response = authenticated_client.post(
        f"/organizations/{ORGANIZATION_ID}/assign-role",
        json=ROLE_PAYLOAD,
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "Permission denied"
    )

    assign_role.assert_not_called()


def test_assign_role_invalid_payload(
    authenticated_client,
    mocker,
):
    permission_override = Mock(
        return_value={
            "id": str(ORGANIZATION_ID),
            "name": "Test Hospital",
        }
    )

    _override_manage_organization_permission(
        permission_override
    )

    response = authenticated_client.post(
        f"/organizations/{ORGANIZATION_ID}/assign-role",
        json={
            "user_id": "not-a-uuid",
            "role_name": "practitioner",
            "org_id": str(ORGANIZATION_ID),
        },
    )

    assert response.status_code == 422


# ============================================================
# INVITE USER
# ============================================================


def test_invite_user_success(
    authenticated_client,
    mocker,
):
    permission_override = Mock(
        return_value={
            "id": str(ORGANIZATION_ID),
            "name": "Test Hospital",
        }
    )

    _override_manage_organization_permission(
        permission_override
    )

    mock_get_org_id = mocker.patch.object(
        router,
        "get_user_organization_id",
        return_value=str(ORGANIZATION_ID),
    )

    mock_create_invitation = mocker.patch.object(
        router,
        "create_invitation",
        return_value={
            "id": "invite-1",
            "email": "staff@test.com",
            "organization_id": str(ORGANIZATION_ID),
            "role_name": "staff",
        },
    )

    response = authenticated_client.post(
        f"/organizations/{ORGANIZATION_ID}/invite",
        json=INVITE_PAYLOAD,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["email"] == "staff@test.com"
    assert body["organization_id"] == str(
        ORGANIZATION_ID
    )

    mock_get_org_id.assert_called_once_with(
        str(USER_ID)
    )

    mock_create_invitation.assert_called_once_with(
        str(ORGANIZATION_ID),
        "staff@test.com",
        "staff",
        str(USER_ID),
    )


def test_invite_user_to_another_organization(
    authenticated_client,
    mocker,
):
    permission_override = Mock(
        return_value={
            "id": str(ORGANIZATION_ID),
            "name": "Test Hospital",
        }
    )

    _override_manage_organization_permission(
        permission_override
    )

    mocker.patch.object(
        router,
        "get_user_organization_id",
        return_value=str(ORGANIZATION_ID),
    )

    create_invitation = mocker.patch.object(
        router,
        "create_invitation",
    )

    other_org_id = (
        "22222222-2222-2222-2222-222222222222"
    )

    response = authenticated_client.post(
        f"/organizations/{other_org_id}/invite",
        json={
            "email": "staff@test.com",
            "role_name": "staff",
            "org_id": other_org_id,
        },
    )

    assert response.status_code == 403

    assert response.json()["detail"] == (
        "Cannot invite users to another organization."
    )

    create_invitation.assert_not_called()


def test_invite_user_permission_denied(
    authenticated_client,
    mocker,
):
    permission_override = Mock(
        side_effect=HTTPException(
            status_code=403,
            detail="Permission denied",
        )
    )

    _override_manage_organization_permission(
        permission_override
    )

    create_invitation = mocker.patch.object(
        router,
        "create_invitation",
    )

    response = authenticated_client.post(
        f"/organizations/{ORGANIZATION_ID}/invite",
        json=INVITE_PAYLOAD,
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "Permission denied"
    )

    create_invitation.assert_not_called()


def test_invite_user_invalid_payload(
    authenticated_client,
    mocker,
):
    permission_override = Mock(
        return_value={
            "id": str(ORGANIZATION_ID),
            "name": "Test Hospital",
        }
    )

    _override_manage_organization_permission(
        permission_override
    )

    response = authenticated_client.post(
        f"/organizations/{ORGANIZATION_ID}/invite",
        json={
            "email": "not-an-email",
            "role_name": "staff",
            "org_id": str(ORGANIZATION_ID),
        },
    )

    assert response.status_code == 422


# ============================================================
# ACCEPT INVITATION
# ============================================================


def test_accept_invitation_success(
    client,
    mocker,
):
    accept_invitation = mocker.patch.object(
        router,
        "accept_invitation",
        return_value={
            "message": "Account created successfully",
            "user_id": str(USER_ID),
        },
    )

    response = client.post(
        "/organizations/accept-invite",
        json=ACCEPT_INVITE_PAYLOAD,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == (
        "Account created successfully"
    )
    assert body["user_id"] == str(USER_ID)

    accept_invitation.assert_called_once()

    payload = accept_invitation.call_args.args[0]

    assert payload.token == (
        ACCEPT_INVITE_PAYLOAD["token"]
    )
    assert payload.password == (
        ACCEPT_INVITE_PAYLOAD["password"]
    )


def test_accept_invitation_invalid_payload(
    client,
):
    response = client.post(
        "/organizations/accept-invite",
        json={
            "token": "",
        },
    )

    assert response.status_code == 422


def test_accept_invitation_service_exception_propagates(
    client,
    mocker,
):
    mocker.patch.object(
        router,
        "accept_invitation",
        side_effect=HTTPException(
            status_code=400,
            detail="Invalid or expired invitation",
        ),
    )

    response = client.post(
        "/organizations/accept-invite",
        json=ACCEPT_INVITE_PAYLOAD,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Invalid or expired invitation"
    )


# ============================================================
# AUTHENTICATION
# ============================================================


@pytest.mark.parametrize(
    "method,url",
    [
        (
            "GET",
            "/organizations/me",
        ),
        (
            "POST",
            "/organizations/upload-logo",
        ),
    ],
)
def test_authenticated_organization_routes_require_authentication(
    client,
    method,
    url,
):
    if method == "GET":
        response = client.get(url)
    else:
        response = client.post(
            url,
            files={
                "file": (
                    "logo.png",
                    b"\x89PNG\r\n\x1a\nfake",
                    "image/png",
                )
            },
        )

    assert response.status_code == 401


# ============================================================
# PERMISSION DEPENDENCY — REAL GUARD
# ============================================================


def test_manage_organization_permission_dependency_is_registered():
    dependency = _find_manage_organization_dependency()

    assert dependency is not None


def test_manage_organization_permission_denies_without_roles(
    authenticated_client,
    mocker,
):
    """
    This test exercises the actual require_permission()
    implementation rather than replacing it.

    The dependency should reject the request when Supabase
    returns no matching user_roles rows.
    """

    permission_query = Mock()

    permission_query.select.return_value = permission_query
    permission_query.eq.return_value = permission_query
    permission_query.execute.return_value = Mock(
        data=[]
    )

    supabase = mocker.patch(
        "app.core.security.supabase"
    )

    supabase.table.return_value = permission_query

    response = authenticated_client.put(
        "/organizations/update",
        json=UPDATE_PAYLOAD,
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "No roles in this organization"
    )

    supabase.table.assert_called_once_with(
        "user_roles"
    )

    permission_query.select.assert_called_once()


def test_manage_organization_permission_denies_missing_permission(
    authenticated_client,
    mocker,
):
    permission_query = Mock()

    permission_query.select.return_value = permission_query
    permission_query.eq.return_value = permission_query
    permission_query.execute.return_value = Mock(
        data=[
            {
                "organization_id": str(ORGANIZATION_ID),
                "roles": {
                    "name": "staff",
                    "role_permissions": [
                        {
                            "permissions": {
                                "name": "view_organization"
                            }
                        }
                    ],
                },
            }
        ]
    )

    supabase = mocker.patch(
        "app.core.security.supabase"
    )

    supabase.table.return_value = permission_query

    response = authenticated_client.put(
        "/organizations/update",
        json=UPDATE_PAYLOAD,
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "Permission denied"
    )


def test_manage_organization_permission_allows_matching_permission(
    authenticated_client,
    mocker,
):
    permission_query = Mock()

    permission_query.select.return_value = permission_query
    permission_query.eq.return_value = permission_query
    permission_query.execute.return_value = Mock(
        data=[
            {
                "organization_id": str(ORGANIZATION_ID),
                "roles": {
                    "name": "org_admin",
                    "role_permissions": [
                        {
                            "permissions": {
                                "name": "manage_organization"
                            }
                        }
                    ],
                },
            }
        ]
    )

    supabase = mocker.patch(
        "app.core.security.supabase"
    )

    supabase.table.return_value = permission_query

    mocker.patch.object(
        router,
        "get_user_organization_id",
        return_value=str(ORGANIZATION_ID),
    )

    mock_update = mocker.patch.object(
        router,
        "update_organization",
        return_value={
            "id": str(ORGANIZATION_ID),
            "name": "Updated Hospital",
        },
    )

    response = authenticated_client.put(
        "/organizations/update",
        json=UPDATE_PAYLOAD,
    )

    assert response.status_code == 200

    mock_update.assert_called_once()