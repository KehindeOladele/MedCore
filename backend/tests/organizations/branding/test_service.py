from datetime import datetime, timezone
import pytest
from tests.factories.constants import (
    ORGANIZATION_ID,
    USER_ID
)
from app.modules.organizations import queries as organization_queries
from app.modules.organizations.exceptions import (
    OrganizationInactiveError,
    OrganizationNotFoundError,
)
from app.modules.organizations.branding import service 
from app.core.events.schemas import EventTypes
from app.modules.organizations.branding.exceptions import (
    BrandingNotFoundError,
)
from app.modules.organizations.branding.schemas import BrandingThemeUpdate


# ====================================================================================
# TEST CONSTANTS / FACTORIES
# ====================================================================================

ORGANIZATION_ID = ORGANIZATION_ID
USER_ID = USER_ID

NEW_LOGO_PATH = f"{ORGANIZATION_ID}/logo.png"
NEW_LOGO_URL = "https://storage.example.com/logo.png"

OLD_LOGO_PATH = f"{ORGANIZATION_ID}/logo.jpg"
OLD_LOGO_URL = "https://storage.example.com/logo.jpg"


def active_organization():
    return {
        "id": str(ORGANIZATION_ID),
        "active": True,
    }


def inactive_organization():
    return {
        "id": str(ORGANIZATION_ID),
        "active": False,
    }


def branding_record(
    *,
    logo_url=OLD_LOGO_URL,
    logo_path=OLD_LOGO_PATH,
    primary_color="#FFFFFF",
    secondary_color="#000000",
):
    return {
        "id": str(ORGANIZATION_ID),
        "logo_url": logo_url,
        "logo_path": logo_path,
        "primary_color": primary_color,
        "secondary_color": secondary_color,
    }


# ====================================================================================
# _validate_active_organization()
# ====================================================================================


def test_validate_active_organization_succeeds_for_active_organization(mocker):
    get_organization = mocker.patch.object(
        organization_queries,
        "get_organization",
        return_value=active_organization(),
    )

    service._validate_active_organization(ORGANIZATION_ID)

    get_organization.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
    )


def test_validate_active_organization_raises_when_organization_not_found(mocker):
    mocker.patch.object(
        organization_queries,
        "get_organization",
        return_value=None,
    )

    with pytest.raises(OrganizationNotFoundError):
        service._validate_active_organization(ORGANIZATION_ID)


def test_validate_active_organization_raises_when_organization_inactive(mocker):
    mocker.patch.object(
        organization_queries,
        "get_organization",
        return_value=inactive_organization(),
    )

    with pytest.raises(OrganizationInactiveError):
        service._validate_active_organization(ORGANIZATION_ID)


# ====================================================================================
# _response()
# ====================================================================================


def test_response_converts_organization_id_to_string():
    record = branding_record()

    response = service._response(record)

    assert response.organization_id == str(ORGANIZATION_ID)
    assert response.logo_url == OLD_LOGO_URL
    assert response.primary_color == "#FFFFFF"
    assert response.secondary_color == "#000000"


def test_response_allows_missing_optional_branding_values():
    record = {
        "id": str(ORGANIZATION_ID),
        "logo_url": None,
        "primary_color": None,
        "secondary_color": None,
    }

    response = service._response(record)

    assert response.organization_id == str(ORGANIZATION_ID)
    assert response.logo_url is None
    assert response.primary_color is None
    assert response.secondary_color is None


# ====================================================================================
# _record_activity()
# ====================================================================================


def test_record_activity(mocker):
    log_audit_event = mocker.patch.object(
        service,
        "log_audit_event",
    )

    emit_event = mocker.patch.object(
        service,
        "emit_event",
    )

    metadata = {
        "updated_fields": [
            "primary_color",
        ],
    }

    service._record_activity(
        action="organization.branding.updated",
        event_type=EventTypes.ORGANIZATION_BRANDING_UPDATED,
        organization_id=ORGANIZATION_ID,
        actor_id=USER_ID,
        metadata=metadata,
    )

    log_audit_event.assert_called_once_with(
        actor_id=str(USER_ID),
        actor_type="user",
        organization_id=str(ORGANIZATION_ID),
        action="organization.branding.updated",
        resource_type="organization_branding",
        resource_id=str(ORGANIZATION_ID),
        metadata=metadata,
    )

    emit_event.assert_called_once_with(
        aggregate_type="organization",
        aggregate_id=str(ORGANIZATION_ID),
        event_type=EventTypes.ORGANIZATION_BRANDING_UPDATED,
        payload={
            "aggregate_type": "organization",
            "aggregate_id": str(ORGANIZATION_ID),
            "organization_id": str(ORGANIZATION_ID),
            "actor_id": str(USER_ID),
            **metadata,
        },
    )

# ====================================================================================
# get_organization_branding()
# ====================================================================================


def test_get_organization_branding_returns_branding(mocker):
    mocker.patch.object(
        service,
        "_validate_active_organization",
    )

    branding = branding_record()

    get_branding = mocker.patch.object(
        service.queries,
        "get_branding",
        return_value=branding,
    )

    result = service.get_organization_branding(
        organization_id=ORGANIZATION_ID,
    )

    assert result.organization_id == str(ORGANIZATION_ID)
    assert result.logo_url == OLD_LOGO_URL
    assert result.primary_color == "#FFFFFF"
    assert result.secondary_color == "#000000"

    get_branding.assert_called_once_with(ORGANIZATION_ID)


def test_get_organization_branding_raises_when_branding_not_found(mocker):
    mocker.patch.object(
        service,
        "_validate_active_organization",
    )

    get_branding = mocker.patch.object(
        service.queries,
        "get_branding",
        return_value=None,
    )

    with pytest.raises(BrandingNotFoundError):
        service.get_organization_branding(
            organization_id=ORGANIZATION_ID,
        )

    get_branding.assert_called_once_with(ORGANIZATION_ID)


def test_get_organization_branding_validates_organization_first(mocker):
    validate = mocker.patch.object(
        service,
        "_validate_active_organization",
    )

    mocker.patch.object(
        service.queries,
        "get_branding",
        return_value=branding_record(),
    )

    service.get_organization_branding(
        organization_id=ORGANIZATION_ID,
    )

    validate.assert_called_once_with(ORGANIZATION_ID)


# ====================================================================================
# update_theme()
# ====================================================================================


def test_update_theme_updates_primary_color(mocker):
    mocker.patch.object(
        service,
        "_validate_active_organization",
    )

    updated = branding_record(
        primary_color="#FF0000",
    )

    update_branding = mocker.patch.object(
        service.queries,
        "update_branding",
        return_value=updated,
    )

    record_activity = mocker.patch.object(
        service,
        "_record_activity",
    )

    payload = BrandingThemeUpdate(
        primary_color="#ff0000",
    )

    result = service.update_theme(
        organization_id=ORGANIZATION_ID,
        payload=payload,
        actor_id=USER_ID,
    )

    assert result.primary_color == "#FF0000"

    update_branding.assert_called_once()

    updates = update_branding.call_args.args[1]

    assert updates["primary_color"] == "#FF0000"
    assert "updated_at" in updates

    datetime.fromisoformat(updates["updated_at"])

    record_activity.assert_called_once_with(
        action="organization.branding.updated",
        event_type=EventTypes.ORGANIZATION_BRANDING_UPDATED,
        organization_id=ORGANIZATION_ID,
        actor_id=USER_ID,
        metadata={
            "updated_fields": [
                "primary_color",
            ],
        },
    )


def test_update_theme_updates_only_explicitly_supplied_fields(mocker):
    mocker.patch.object(
        service,
        "_validate_active_organization",
    )

    update_branding = mocker.patch.object(
        service.queries,
        "update_branding",
        return_value=branding_record(
            primary_color="#FF0000",
        ),
    )

    mocker.patch.object(
        service,
        "_record_activity",
    )

    payload = BrandingThemeUpdate(
        primary_color="#FF0000",
    )

    service.update_theme(
        organization_id=ORGANIZATION_ID,
        payload=payload,
        actor_id=USER_ID,
    )

    updates = update_branding.call_args.args[1]

    assert updates["primary_color"] == "#FF0000"
    assert "secondary_color" not in updates
    assert "updated_at" in updates


def test_update_theme_updates_both_colors(mocker):
    mocker.patch.object(
        service,
        "_validate_active_organization",
    )

    update_branding = mocker.patch.object(
        service.queries,
        "update_branding",
        return_value=branding_record(
            primary_color="#FF0000",
            secondary_color="#00FF00",
        ),
    )

    mocker.patch.object(
        service,
        "_record_activity",
    )

    payload = BrandingThemeUpdate(
        primary_color="#FF0000",
        secondary_color="#00FF00",
    )

    result = service.update_theme(
        organization_id=ORGANIZATION_ID,
        payload=payload,
        actor_id=USER_ID,
    )

    assert result.primary_color == "#FF0000"
    assert result.secondary_color == "#00FF00"

    updates = update_branding.call_args.args[1]

    assert updates["primary_color"] == "#FF0000"
    assert updates["secondary_color"] == "#00FF00"


def test_update_theme_raises_when_branding_update_returns_none(mocker):
    mocker.patch.object(
        service,
        "_validate_active_organization",
    )

    update_branding = mocker.patch.object(
        service.queries,
        "update_branding",
        return_value=None,
    )

    record_activity = mocker.patch.object(
        service,
        "_record_activity",
    )

    payload = BrandingThemeUpdate(
        primary_color="#FF0000",
    )

    with pytest.raises(BrandingNotFoundError):
        service.update_theme(
            organization_id=ORGANIZATION_ID,
            payload=payload,
            actor_id=USER_ID,
        )

    update_branding.assert_called_once()
    record_activity.assert_not_called()


# ====================================================================================
# upload_logo()
# ====================================================================================


def test_upload_logo_replaces_logo_and_records_activity(mocker):
    mocker.patch.object(
        service,
        "_validate_active_organization",
    )

    current = branding_record()

    get_branding = mocker.patch.object(
        service.queries,
        "get_branding",
        return_value=current,
    )

    replace_logo = mocker.patch.object(
        service.storage,
        "replace_logo",
        return_value=(NEW_LOGO_PATH, NEW_LOGO_URL),
    )

    update_branding = mocker.patch.object(
        service.queries,
        "update_branding",
        return_value=branding_record(
            logo_path=NEW_LOGO_PATH,
            logo_url=NEW_LOGO_URL,
        ),
    )

    delete_logo = mocker.patch.object(
        service.storage,
        "delete_logo",
    )

    record_activity = mocker.patch.object(
        service,
        "_record_activity",
    )

    content = b"logo-content"

    result = service.upload_logo(
        organization_id=ORGANIZATION_ID,
        content_type="image/png",
        content=content,
        actor_id=USER_ID,
    )

    assert result.organization_id == str(ORGANIZATION_ID)
    assert result.logo_url == NEW_LOGO_URL

    get_branding.assert_called_once_with(ORGANIZATION_ID)

    replace_logo.assert_called_once_with(
        organization_id=ORGANIZATION_ID,
        content_type="image/png",
        content=content,
    )

    updates = update_branding.call_args.args[1]

    assert updates["logo_path"] == NEW_LOGO_PATH
    assert updates["logo_url"] == NEW_LOGO_URL
    assert "updated_at" in updates

    delete_logo.assert_called_once_with(OLD_LOGO_PATH)

    record_activity.assert_called_once_with(
        action="organization.branding.logo_updated",
        event_type=EventTypes.ORGANIZATION_LOGO_UPDATED,
        organization_id=ORGANIZATION_ID,
        actor_id=USER_ID,
        metadata={
            "logo_path": NEW_LOGO_PATH,
        },
    )


def test_upload_logo_raises_when_current_branding_not_found(mocker):
    mocker.patch.object(
        service,
        "_validate_active_organization",
    )

    get_branding = mocker.patch.object(
        service.queries,
        "get_branding",
        return_value=None,
    )

    replace_logo = mocker.patch.object(
        service.storage,
        "replace_logo",
    )

    with pytest.raises(BrandingNotFoundError):
        service.upload_logo(
            organization_id=ORGANIZATION_ID,
            content_type="image/png",
            content=b"logo-content",
            actor_id=USER_ID,
        )

    get_branding.assert_called_once_with(ORGANIZATION_ID)
    replace_logo.assert_not_called()


def test_upload_logo_deletes_new_logo_when_database_update_fails(mocker):
    mocker.patch.object(
        service,
        "_validate_active_organization",
    )

    mocker.patch.object(
        service.queries,
        "get_branding",
        return_value=branding_record(),
    )

    replace_logo = mocker.patch.object(
        service.storage,
        "replace_logo",
        return_value=(NEW_LOGO_PATH, NEW_LOGO_URL),
    )

    update_branding = mocker.patch.object(
        service.queries,
        "update_branding",
        return_value=None,
    )

    delete_logo = mocker.patch.object(
        service.storage,
        "delete_logo",
    )

    record_activity = mocker.patch.object(
        service,
        "_record_activity",
    )

    with pytest.raises(BrandingNotFoundError):
        service.upload_logo(
            organization_id=ORGANIZATION_ID,
            content_type="image/png",
            content=b"logo-content",
            actor_id=USER_ID,
        )

    replace_logo.assert_called_once()

    update_branding.assert_called_once()

    delete_logo.assert_called_once_with(
        NEW_LOGO_PATH,
    )

    record_activity.assert_not_called()


def test_upload_logo_does_not_delete_old_logo_when_no_old_logo_exists(mocker):
    mocker.patch.object(
        service,
        "_validate_active_organization",
    )

    mocker.patch.object(
        service.queries,
        "get_branding",
        return_value=branding_record(
            logo_path=None,
            logo_url=None,
        ),
    )

    mocker.patch.object(
        service.storage,
        "replace_logo",
        return_value=(NEW_LOGO_PATH, NEW_LOGO_URL),
    )

    mocker.patch.object(
        service.queries,
        "update_branding",
        return_value=branding_record(
            logo_path=NEW_LOGO_PATH,
            logo_url=NEW_LOGO_URL,
        ),
    )

    delete_logo = mocker.patch.object(
        service.storage,
        "delete_logo",
    )

    mocker.patch.object(
        service,
        "_record_activity",
    )

    service.upload_logo(
        organization_id=ORGANIZATION_ID,
        content_type="image/png",
        content=b"logo-content",
        actor_id=USER_ID,
    )

    delete_logo.assert_not_called()


def test_upload_logo_does_not_delete_old_logo_when_path_is_unchanged(mocker):
    mocker.patch.object(
        service,
        "_validate_active_organization",
    )

    same_path = NEW_LOGO_PATH

    mocker.patch.object(
        service.queries,
        "get_branding",
        return_value=branding_record(
            logo_path=same_path,
            logo_url=NEW_LOGO_URL,
        ),
    )

    mocker.patch.object(
        service.storage,
        "replace_logo",
        return_value=(same_path, NEW_LOGO_URL),
    )

    mocker.patch.object(
        service.queries,
        "update_branding",
        return_value=branding_record(
            logo_path=same_path,
            logo_url=NEW_LOGO_URL,
        ),
    )

    delete_logo = mocker.patch.object(
        service.storage,
        "delete_logo",
    )

    mocker.patch.object(
        service,
        "_record_activity",
    )

    service.upload_logo(
        organization_id=ORGANIZATION_ID,
        content_type="image/png",
        content=b"logo-content",
        actor_id=USER_ID,
    )

    delete_logo.assert_not_called()


# ====================================================================================
# remove_logo()
# ====================================================================================


def test_remove_logo_deletes_existing_logo_and_clears_database(mocker):
    mocker.patch.object(
        service,
        "_validate_active_organization",
    )

    current = branding_record()

    mocker.patch.object(
        service.queries,
        "get_branding",
        return_value=current,
    )

    delete_logo = mocker.patch.object(
        service.storage,
        "delete_logo",
    )

    update_branding = mocker.patch.object(
        service.queries,
        "update_branding",
        return_value=branding_record(
            logo_path=None,
            logo_url=None,
        ),
    )

    record_activity = mocker.patch.object(
        service,
        "_record_activity",
    )

    result = service.remove_logo(
        organization_id=ORGANIZATION_ID,
        actor_id=USER_ID,
    )

    assert result.organization_id == str(ORGANIZATION_ID)
    assert result.organization_id == str(ORGANIZATION_ID)
    assert result.logo_url is None
    assert result.primary_color == "#FFFFFF"
    assert result.secondary_color == "#000000"

    delete_logo.assert_called_once_with(
        OLD_LOGO_PATH,
    )

    updates = update_branding.call_args.args[1]

    assert updates["logo_path"] is None
    assert updates["logo_url"] is None
    assert "updated_at" in updates

    datetime.fromisoformat(updates["updated_at"])

    record_activity.assert_called_once_with(
        action="organization.branding.logo_removed",
        event_type=service.EventTypes.ORGANIZATION_LOGO_REMOVED,
        organization_id=ORGANIZATION_ID,
        actor_id=USER_ID,
        metadata={},
    )


def test_remove_logo_does_not_delete_storage_when_no_logo_exists(mocker):
    mocker.patch.object(
        service,
        "_validate_active_organization",
    )

    mocker.patch.object(
        service.queries,
        "get_branding",
        return_value=branding_record(
            logo_path=None,
            logo_url=None,
        ),
    )

    delete_logo = mocker.patch.object(
        service.storage,
        "delete_logo",
    )

    update_branding = mocker.patch.object(
        service.queries,
        "update_branding",
        return_value=branding_record(
            logo_path=None,
            logo_url=None,
        ),
    )

    mocker.patch.object(
        service,
        "_record_activity",
    )

    result = service.remove_logo(
        organization_id=ORGANIZATION_ID,
        actor_id=USER_ID,
    )

    assert result.logo_url is None
    delete_logo.assert_not_called()

    updates = update_branding.call_args.args[1]

    assert updates["logo_path"] is None
    assert updates["logo_url"] is None


def test_remove_logo_raises_when_branding_not_found(mocker):
    mocker.patch.object(
        service,
        "_validate_active_organization",
    )

    mocker.patch.object(
        service.queries,
        "get_branding",
        return_value=None,
    )

    delete_logo = mocker.patch.object(
        service.storage,
        "delete_logo",
    )

    update_branding = mocker.patch.object(
        service.queries,
        "update_branding",
    )

    with pytest.raises(BrandingNotFoundError):
        service.remove_logo(
            organization_id=ORGANIZATION_ID,
            actor_id=USER_ID,
        )

    delete_logo.assert_not_called()
    update_branding.assert_not_called()


def test_remove_logo_raises_when_database_update_fails(mocker):
    mocker.patch.object(
        service,
        "_validate_active_organization",
    )

    mocker.patch.object(
        service.queries,
        "get_branding",
        return_value=branding_record(),
    )

    delete_logo = mocker.patch.object(
        service.storage,
        "delete_logo",
    )

    update_branding = mocker.patch.object(
        service.queries,
        "update_branding",
        return_value=None,
    )

    record_activity = mocker.patch.object(
        service,
        "_record_activity",
    )

    with pytest.raises(BrandingNotFoundError):
        service.remove_logo(
            organization_id=ORGANIZATION_ID,
            actor_id=USER_ID,
        )

    delete_logo.assert_called_once_with(
        OLD_LOGO_PATH,
    )

    update_branding.assert_called_once()

    record_activity.assert_not_called()