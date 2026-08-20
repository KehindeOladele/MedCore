import pytest

from app.modules.organizations.branding import storage
from app.modules.organizations.branding.exceptions import InvalidLogoError
from tests.factories.constants import ORGANIZATION_ID


def test_validate_logo_accepts_allowed_image():
    assert storage.validate_logo("image/png", b"\x89PNG\r\n\x1a\nimage") == "png"


@pytest.mark.parametrize("content_type,content", [("image/gif", b"image"), ("image/png", b""), (None, b"image"), ("image/png", b"not-a-png")])
def test_validate_logo_rejects_invalid_uploads(content_type, content):
    with pytest.raises(InvalidLogoError):
        storage.validate_logo(content_type, content)


def test_replace_logo_uploads_to_organization_path(mocker):
    bucket = mocker.Mock()
    bucket.get_public_url.return_value = "https://storage.test/logo.png"
    admin = mocker.patch.object(storage, "supabase_admin")
    admin.storage.from_.return_value = bucket
    path, url = storage.replace_logo(organization_id=ORGANIZATION_ID, content_type="image/png", content=b"\x89PNG\r\n\x1a\nimage")
    assert path == f"{ORGANIZATION_ID}/logo.png"
    assert url == "https://storage.test/logo.png"
    bucket.upload.assert_called_once()


def test_delete_logo_removes_internal_path(mocker):
    bucket = mocker.Mock()
    admin = mocker.patch.object(storage, "supabase_admin")
    admin.storage.from_.return_value = bucket
    storage.delete_logo("org/logo.png")
    bucket.remove.assert_called_once_with(["org/logo.png"])
