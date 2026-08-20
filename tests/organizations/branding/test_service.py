import pytest

from app.modules.organizations.branding import service
from app.modules.organizations.branding.exceptions import BrandingNotFoundError
from app.modules.organizations.branding.schemas import BrandingThemeUpdate
from tests.factories.constants import ORGANIZATION_ID, USER_ID


def branding(**overrides):
    result = {"id": str(ORGANIZATION_ID), "logo_url": None, "logo_path": None, "primary_color": None, "secondary_color": None}
    result.update(overrides)
    return result


def active_organization(mocker):
    mocker.patch.object(service.organization_queries, "get_organization", return_value={"active": True})


def test_get_branding_returns_a_public_contract(mocker):
    active_organization(mocker)
    mocker.patch.object(service.queries, "get_branding", return_value=branding(primary_color="#123456"))
    result = service.get_organization_branding(organization_id=ORGANIZATION_ID)
    assert result.primary_color == "#123456"


def test_update_theme_persists_only_supplied_values_and_records_activity(mocker):
    active_organization(mocker)
    update = mocker.patch.object(service.queries, "update_branding", return_value=branding(primary_color="#123456"))
    activity = mocker.patch.object(service, "_record_activity")
    result = service.update_theme(organization_id=ORGANIZATION_ID, payload=BrandingThemeUpdate(primary_color="#123456"), actor_id=USER_ID)
    assert result.primary_color == "#123456"
    assert update.call_args.args[1]["primary_color"] == "#123456"
    activity.assert_called_once()


def test_upload_logo_replaces_previous_file_after_database_update(mocker):
    active_organization(mocker)
    mocker.patch.object(service.queries, "get_branding", return_value=branding(logo_path="old/logo.png"))
    mocker.patch.object(service.storage, "replace_logo", return_value=("new/logo.png", "https://storage.test/new/logo.png"))
    mocker.patch.object(service.queries, "update_branding", return_value=branding(logo_path="new/logo.png", logo_url="https://storage.test/new/logo.png"))
    delete = mocker.patch.object(service.storage, "delete_logo")
    mocker.patch.object(service, "_record_activity")
    result = service.upload_logo(organization_id=ORGANIZATION_ID, content_type="image/png", content=b"image", actor_id=USER_ID)
    assert result.logo_url == "https://storage.test/new/logo.png"
    delete.assert_called_once_with("old/logo.png")


def test_remove_logo_clears_database_and_storage(mocker):
    active_organization(mocker)
    mocker.patch.object(service.queries, "get_branding", return_value=branding(logo_path="org/logo.png", logo_url="https://storage.test/logo.png"))
    delete = mocker.patch.object(service.storage, "delete_logo")
    mocker.patch.object(service.queries, "update_branding", return_value=branding())
    mocker.patch.object(service, "_record_activity")
    result = service.remove_logo(organization_id=ORGANIZATION_ID, actor_id=USER_ID)
    assert result.logo_url is None
    delete.assert_called_once_with("org/logo.png")


def test_get_branding_raises_when_the_record_is_missing(mocker):
    active_organization(mocker)
    mocker.patch.object(service.queries, "get_branding", return_value=None)
    with pytest.raises(BrandingNotFoundError):
        service.get_organization_branding(organization_id=ORGANIZATION_ID)
