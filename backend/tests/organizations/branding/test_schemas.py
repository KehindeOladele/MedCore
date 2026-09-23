import pytest
from pydantic import ValidationError

from app.modules.organizations.branding.schemas import (
    BrandingResponse,
    BrandingThemeUpdate,
)


# ====================================================================================
# BRANDING THEME UPDATE — VALID INPUT
# ====================================================================================


def test_branding_theme_update_accepts_primary_color():
    payload = BrandingThemeUpdate(primary_color="#ffffff")

    assert payload.primary_color == "#FFFFFF"
    assert payload.secondary_color is None


def test_branding_theme_update_accepts_secondary_color():
    payload = BrandingThemeUpdate(secondary_color="#abcdef")

    assert payload.primary_color is None
    assert payload.secondary_color == "#ABCDEF"


def test_branding_theme_update_accepts_both_colors():
    payload = BrandingThemeUpdate(
        primary_color="#12abef",
        secondary_color="#FEDCBA",
    )

    assert payload.primary_color == "#12ABEF"
    assert payload.secondary_color == "#FEDCBA"


# ====================================================================================
# BRANDING THEME UPDATE — NORMALIZATION
# ====================================================================================


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("#ffffff", "#FFFFFF"),
        ("#abcdef", "#ABCDEF"),
        ("#12abEf", "#12ABEF"),
        ("#123456", "#123456"),
        ("#ABCDEF", "#ABCDEF"),
    ],
)
def test_branding_theme_update_normalizes_colors(value, expected):
    payload = BrandingThemeUpdate(primary_color=value)

    assert payload.primary_color == expected


def test_branding_theme_update_preserves_explicit_none():
    payload = BrandingThemeUpdate(primary_color=None)

    assert payload.primary_color is None
    assert "primary_color" in payload.model_fields_set


def test_branding_theme_update_allows_explicit_none_for_both_fields():
    payload = BrandingThemeUpdate(
        primary_color=None,
        secondary_color=None,
    )

    assert payload.primary_color is None
    assert payload.secondary_color is None
    assert payload.model_fields_set == {
        "primary_color",
        "secondary_color",
    }


# ====================================================================================
# BRANDING THEME UPDATE — EMPTY PAYLOAD
# ====================================================================================


def test_branding_theme_update_rejects_empty_payload():
    with pytest.raises(ValidationError, match="Provide primary_color or secondary_color."):
        BrandingThemeUpdate()


# ====================================================================================
# BRANDING THEME UPDATE — INVALID COLORS
# ====================================================================================


@pytest.mark.parametrize(
    "value",
    [
        "",
        "#",
        "#123",
        "#12345",
        "#1234567",
        "123456",
        "##123456",
        "#12345G",
        "#GGGGGG",
        "red",
        "rgb(255, 0, 0)",
    ],
)
def test_branding_theme_update_rejects_invalid_primary_color(value):
    with pytest.raises(ValidationError):
        BrandingThemeUpdate(primary_color=value)


@pytest.mark.parametrize(
    "value",
    [
        "",
        "#",
        "#123",
        "#12345",
        "#1234567",
        "123456",
        "##123456",
        "#12345G",
        "#GGGGGG",
        "blue",
        "rgb(0, 0, 255)",
    ],
)
def test_branding_theme_update_rejects_invalid_secondary_color(value):
    with pytest.raises(ValidationError):
        BrandingThemeUpdate(secondary_color=value)


# ====================================================================================
# BRANDING RESPONSE
# ====================================================================================


def test_branding_response_accepts_complete_branding():
    response = BrandingResponse(
        organization_id="org-123",
        logo_url="https://storage.example.com/logo.png",
        primary_color="#FFFFFF",
        secondary_color="#000000",
    )

    assert response.organization_id == "org-123"
    assert response.logo_url == "https://storage.example.com/logo.png"
    assert response.primary_color == "#FFFFFF"
    assert response.secondary_color == "#000000"


def test_branding_response_allows_missing_optional_fields():
    response = BrandingResponse(
        organization_id="org-123",
    )

    assert response.organization_id == "org-123"
    assert response.logo_url is None
    assert response.primary_color is None
    assert response.secondary_color is None


def test_branding_response_serializes_expected_fields():
    response = BrandingResponse(
        organization_id="org-123",
        logo_url="https://storage.example.com/logo.png",
        primary_color="#FFFFFF",
        secondary_color="#000000",
    )

    assert response.model_dump() == {
        "organization_id": "org-123",
        "logo_url": "https://storage.example.com/logo.png",
        "primary_color": "#FFFFFF",
        "secondary_color": "#000000",
    }


# ====================================================================================
# BRANDING RESPONSE — FHIR-ALIGNED APPLICATION CONTRACT
# ====================================================================================


def test_branding_response_does_not_expose_internal_logo_path():
    response = BrandingResponse(
        organization_id="org-123",
        logo_url="https://storage.example.com/logo.png",
    )

    assert "logo_path" not in response.model_dump()