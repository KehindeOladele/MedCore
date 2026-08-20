import pytest

from app.modules.organizations.branding import router
from app.modules.organizations.branding.exceptions import BrandingNotFoundError
from tests.factories.constants import ORGANIZATION_ID, USER_ID


BASE_URL = f"/organizations/{ORGANIZATION_ID}/branding"


def branding_response():
    return {"organization_id": str(ORGANIZATION_ID), "logo_url": None, "primary_color": "#123456", "secondary_color": None}


def test_get_branding_delegates_to_service(authenticated_client, mocker):
    get = mocker.patch.object(router, "get_organization_branding", return_value=branding_response())
    response = authenticated_client.get(BASE_URL)
    assert response.status_code == 200
    get.assert_called_once_with(organization_id=ORGANIZATION_ID)


def test_update_theme_delegates_to_service(authenticated_client, mocker):
    update = mocker.patch.object(router, "update_theme", return_value=branding_response())
    response = authenticated_client.put(f"{BASE_URL}/theme", json={"primary_color": "#123456"})
    assert response.status_code == 200
    update.assert_called_once_with(organization_id=ORGANIZATION_ID, payload=mocker.ANY, actor_id=USER_ID)


def test_upload_logo_delegates_to_service(authenticated_client, mocker):
    upload = mocker.patch.object(router, "upload_logo", return_value=branding_response())
    response = authenticated_client.put(f"{BASE_URL}/logo", files={"file": ("logo.png", b"image", "image/png")})
    assert response.status_code == 200
    upload.assert_called_once_with(organization_id=ORGANIZATION_ID, content_type="image/png", content=b"image", actor_id=USER_ID)


def test_remove_logo_returns_no_content(authenticated_client, mocker):
    remove = mocker.patch.object(router, "remove_logo")
    response = authenticated_client.delete(f"{BASE_URL}/logo")
    assert response.status_code == 204
    remove.assert_called_once_with(organization_id=ORGANIZATION_ID, actor_id=USER_ID)


def test_missing_branding_is_404(authenticated_client, mocker):
    mocker.patch.object(router, "get_organization_branding", side_effect=BrandingNotFoundError())
    assert authenticated_client.get(BASE_URL).status_code == 404


@pytest.mark.parametrize("method,path", [("GET", BASE_URL), ("PUT", f"{BASE_URL}/theme"), ("PUT", f"{BASE_URL}/logo"), ("DELETE", f"{BASE_URL}/logo")])
def test_routes_require_authentication(client, method, path):
    assert client.request(method, path).status_code == 401
