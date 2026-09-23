from uuid import UUID

import pytest
from tests.factories.constants import (
    ORGANIZATION_ID,
    USER_ID
)
from tests.fixtures.auth import (
    authenticated_client
)
from app.modules.organizations.branding import router
from tests.factories.branding import branding_response
from app.modules.organizations.branding import router


# ====================================================================================
# TEST CONSTANTS
# ====================================================================================

ORGANIZATION_ID = ORGANIZATION_ID
USER_ID = USER_ID
BASE_URL= f"/organizations/{ORGANIZATION_ID}/branding"

# ====================================================================================
# GET BRANDING
# ====================================================================================


def test_get_branding_endpoint_delegates_to_service(
    authenticated_client,
    mocker,
):
    mock_get_branding = mocker.patch.object(
        router,
        "get_organization_branding",
        return_value=branding_response(),
    )

    response = authenticated_client.get(
        BASE_URL,
    )

    assert response.status_code == 200

    assert response.json() == {
        "organization_id": str(ORGANIZATION_ID),
        "logo_url": "https://example.com/logo.png",
        "primary_color": "#FFFFFF",
        "secondary_color": "#000000",
    }

    mock_get_branding.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
    )


# ====================================================================================
# UPDATE BRANDING THEME
# ====================================================================================

def test_update_theme_endpoint_delegates_to_service(
    authenticated_client,
    mocker,
):
    mock_update_theme = mocker.patch.object(
        router,
        "update_theme",
        return_value=branding_response(),
    )

    response = authenticated_client.put(
        f"{BASE_URL}/theme",
        json={
            "primary_color": "#ff0000",
            "secondary_color": "#00ff00",
        },
    )

    assert response.status_code == 200

    mock_update_theme.assert_called_once()

    call_kwargs = mock_update_theme.call_args.kwargs

    assert call_kwargs["organization_id"] == ORGANIZATION_ID
    assert call_kwargs["actor_id"] == USER_ID

    payload = call_kwargs["payload"]

    assert payload.primary_color == "#FF0000"
    assert payload.secondary_color == "#00FF00"


# ====================================================================================
# UPLOAD ORGANIZATION LOGO
# ====================================================================================


def test_upload_logo_endpoint_delegates_to_service(
    authenticated_client,
    mocker,
):
    mock_upload_logo = mocker.patch.object(
        router,
        "upload_logo",
        return_value=branding_response(),
    )

    content = b"\x89PNG\r\n\x1a\nfake-png-content"

    response = authenticated_client.put(
        f"{BASE_URL}/logo",
        files={
            "file": (
                "logo.png",
                content,
                "image/png",
            )
        },
    )

    assert response.status_code == 200

    mock_upload_logo.assert_called_once()

    call_kwargs = mock_upload_logo.call_args.kwargs

    assert call_kwargs["organization_id"] == ORGANIZATION_ID
    assert call_kwargs["content_type"] == "image/png"
    assert call_kwargs["content"] == content
    assert call_kwargs["actor_id"] == USER_ID

# ====================================================================================
# REMOVE ORGANIZATION LOGO
# ====================================================================================


def test_remove_logo_endpoint_delegates_to_service(
    authenticated_client,
    mocker,
):
    mock_remove_logo = mocker.patch.object(
        router,
        "remove_logo",
    )

    response = authenticated_client.delete(
        f"{BASE_URL}/logo",
    )

    assert response.status_code == 204
    assert response.content == b""

    mock_remove_logo.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
        actor_id=USER_ID,
    )


# ====================================================================================
# THEME VALIDATION
# ====================================================================================


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"primary_color": "red"},
        {"primary_color": "#123"},
        {"primary_color": "#GGGGGG"},
        {"secondary_color": "blue"},
        {"secondary_color": "#12345"},
    ],
)
def test_update_theme_endpoint_rejects_invalid_payload(
    mocker,
    payload,
    authenticated_client
):

    mock_update_theme = mocker.patch.object(
        router,
        "update_theme",
        return_value=branding_response(),
    )


    response = authenticated_client.put(
        f"{BASE_URL}/theme",
        json=payload,
    )

    assert response.status_code == 422
    mock_update_theme.assert_not_called()


# ====================================================================================
# LOGO UPLOAD VALIDATION / REQUEST WIRING
# ====================================================================================


def test_upload_logo_endpoint_requires_file(
        authenticated_client,
        mocker,
        ):

    mock_upload_logo = mocker.patch.object(
        router,
        "upload_logo",
        return_value=branding_response(),
    )

    response = authenticated_client.put(
        f"{BASE_URL}/logo",
    )

    assert response.status_code == 422
    mock_upload_logo.assert_not_called()


def test_upload_logo_endpoint_forwards_empty_file(
        authenticated_client,
        mocker,
        ):

    mock_upload_logo = mocker.patch.object(
        router,
        "upload_logo",
        return_value=branding_response(),
    )

    response = authenticated_client.put(
        f"{BASE_URL}/logo",
        files={
            "file": (
                "empty.png",
                b"",
                "image/png",
            )
        },
    )

    assert response.status_code == 200

    mock_upload_logo.assert_called_once()

    call_kwargs = mock_upload_logo.call_args.kwargs

    assert call_kwargs["organization_id"] == ORGANIZATION_ID
    assert call_kwargs["content_type"] == "image/png"
    assert call_kwargs["content"] == b""
    assert call_kwargs["actor_id"] == USER_ID


# ====================================================================================
# UUID PATH VALIDATION
# ====================================================================================


def test_get_branding_endpoint_rejects_invalid_organization_id(authenticated_client):

    response = authenticated_client.get(
        "/organizations/not-a-uuid/branding",
    )

    assert response.status_code == 422


def test_update_theme_endpoint_rejects_invalid_organization_id(authenticated_client):

    response = authenticated_client.put(
        "/organizations/not-a-uuid/branding/theme",
        json={
            "primary_color": "#FFFFFF",
        },
    )

    assert response.status_code == 422


def test_upload_logo_endpoint_rejects_invalid_organization_id(authenticated_client):

    response = authenticated_client.put(
        "/organizations/not-a-uuid/branding/logo",
        files={
            "file": (
                "logo.png",
                b"content",
                "image/png",
            )
        },
    )

    assert response.status_code == 422


def test_remove_logo_endpoint_rejects_invalid_organization_id(authenticated_client):

    response = authenticated_client.delete(
        "/organizations/not-a-uuid/branding/logo",
    )

    assert response.status_code == 422