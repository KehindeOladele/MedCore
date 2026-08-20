import pytest
from pydantic import ValidationError

from app.modules.organizations.branding.schemas import BrandingThemeUpdate


def test_theme_requires_at_least_one_field():
    with pytest.raises(ValidationError, match="Provide"):
        BrandingThemeUpdate()


def test_theme_normalizes_hex_colors():
    theme = BrandingThemeUpdate(primary_color="#12abef", secondary_color="#aabbcc")
    assert theme.primary_color == "#12ABEF"
    assert theme.secondary_color == "#AABBCC"


@pytest.mark.parametrize("value", ["12ABEF", "#123", "#GGGGGG", "#1234567"])
def test_theme_rejects_invalid_hex_colors(value):
    with pytest.raises(ValidationError):
        BrandingThemeUpdate(primary_color=value)
