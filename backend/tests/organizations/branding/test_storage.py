import pytest
from unittest.mock import Mock
from uuid import uuid4
from tests.factories.constants import ORGANIZATION_ID
from app.modules.organizations.branding.constants import (
    MAX_LOGO_SIZE_BYTES,
)
from app.modules.organizations.branding.exceptions import InvalidLogoError
from app.modules.organizations.branding.storage import validate_logo
from app.modules.organizations.branding.constants import BUCKET
from app.modules.organizations.branding.storage import (
    delete_logo,
    replace_logo,
)

# ====================================================================================
# VALID LOGO SIGNATURES
# ====================================================================================


def test_validate_logo_accepts_valid_png():
    content = b"\x89PNG\r\n\x1a\n" + b"png-content"

    extension = validate_logo(
        content_type="image/png",
        content=content,
    )

    assert extension == "png"


def test_validate_logo_accepts_valid_jpeg():
    content = b"\xff\xd8\xff" + b"jpeg-content"

    extension = validate_logo(
        content_type="image/jpeg",
        content=content,
    )

    assert extension == "jpg"


def test_validate_logo_accepts_valid_webp():
    content = (
        b"RIFF"
        + b"\x00\x00\x00\x00"
        + b"WEBP"
        + b"webp-content"
    )

    extension = validate_logo(
        content_type="image/webp",
        content=content,
    )

    assert extension == "webp"


# ====================================================================================
# INVALID SIGNATURES
# ====================================================================================


def test_validate_logo_rejects_invalid_png_signature():
    content = b"NOTPNG" + b"png-content"

    with pytest.raises(InvalidLogoError):
        validate_logo(
            content_type="image/png",
            content=content,
        )


def test_validate_logo_rejects_invalid_jpeg_signature():
    content = b"NOTJPEG" + b"jpeg-content"

    with pytest.raises(InvalidLogoError):
        validate_logo(
            content_type="image/jpeg",
            content=content,
        )


def test_validate_logo_rejects_invalid_webp_signature():
    content = (
        b"RIFF"
        + b"\x00\x00\x00\x00"
        + b"NOPE"
        + b"webp-content"
    )

    with pytest.raises(InvalidLogoError):
        validate_logo(
            content_type="image/webp",
            content=content,
        )


# ====================================================================================
# MIME TYPE / SIGNATURE MISMATCHES
# ====================================================================================


@pytest.mark.parametrize(
    ("content_type", "content"),
    [
        ("image/png", b"\xff\xd8\xff" + b"jpeg-content"),
        ("image/png", b"RIFF" + b"\x00\x00\x00\x00" + b"WEBP"),
        ("image/jpeg", b"\x89PNG\r\n\x1a\n" + b"png-content"),
        ("image/jpeg", b"RIFF" + b"\x00\x00\x00\x00" + b"WEBP"),
        ("image/webp", b"\x89PNG\r\n\x1a\n" + b"png-content"),
        ("image/webp", b"\xff\xd8\xff" + b"jpeg-content"),
    ],
)
def test_validate_logo_rejects_mime_signature_mismatch(
    content_type,
    content,
):
    with pytest.raises(InvalidLogoError):
        validate_logo(
            content_type=content_type,
            content=content,
        )


# ====================================================================================
# EMPTY / MISSING CONTENT
# ====================================================================================


@pytest.mark.parametrize(
    "content",
    [
        b"",
    ],
)
def test_validate_logo_rejects_empty_content(content):
    with pytest.raises(InvalidLogoError):
        validate_logo(
            content_type="image/png",
            content=content,
        )


# ====================================================================================
# SIZE BOUNDARIES
# ====================================================================================


def test_validate_logo_accepts_content_at_maximum_size():
    content = b"\x89PNG\r\n\x1a\n" + b"x" * (
        MAX_LOGO_SIZE_BYTES - len(b"\x89PNG\r\n\x1a\n")
    )

    extension = validate_logo(
        content_type="image/png",
        content=content,
    )

    assert extension == "png"
    assert len(content) == MAX_LOGO_SIZE_BYTES


def test_validate_logo_rejects_content_over_maximum_size():
    content = b"\x89PNG\r\n\x1a\n" + b"x" * (
        MAX_LOGO_SIZE_BYTES - len(b"\x89PNG\r\n\x1a\n") + 1
    )

    with pytest.raises(InvalidLogoError):
        validate_logo(
            content_type="image/png",
            content=content,
        )


# ====================================================================================
# UNSUPPORTED / MISSING CONTENT TYPES
# ====================================================================================


@pytest.mark.parametrize(
    "content_type",
    [
        None,
        "",
        "image/gif",
        "image/bmp",
        "image/svg+xml",
        "application/octet-stream",
        "text/plain",
    ],
)
def test_validate_logo_rejects_unsupported_content_type(content_type):
    content = b"\x89PNG\r\n\x1a\n" + b"png-content"

    with pytest.raises(InvalidLogoError):
        validate_logo(
            content_type=content_type,
            content=content,
        )

# ====================================================================================
# REPLACE ORGANIZATION LOGO
# ====================================================================================


def test_replace_logo_uploads_to_expected_bucket_and_path(monkeypatch):
    organization_id = ORGANIZATION_ID
    content = b"\x89PNG\r\n\x1a\n" + b"png-content"

    bucket = Mock()
    bucket.get_public_url.return_value = (
        f"https://storage.example.com/{organization_id}/logo.png"
    )

    storage = Mock()
    storage.from_.return_value = bucket

    supabase = Mock()
    supabase.storage = storage

    monkeypatch.setattr(
        "app.modules.organizations.branding.storage.supabase_admin",
        supabase,
    )

    path, url = replace_logo(
        organization_id=organization_id,
        content_type="image/png",
        content=content,
    )

    expected_path = f"{organization_id}/logo.png"

    assert path == expected_path
    assert url == f"https://storage.example.com/{expected_path}"

    storage.from_.assert_called_once_with(BUCKET)

    bucket.upload.assert_called_once_with(
        path=expected_path,
        file=content,
        file_options={
            "content-type": "image/png",
            "upsert": "true",
        },
    )

    bucket.get_public_url.assert_called_once_with(expected_path)


def test_replace_logo_uses_jpg_extension_for_jpeg(monkeypatch):
    organization_id = uuid4()
    content = b"\xff\xd8\xff" + b"jpeg-content"

    bucket = Mock()
    bucket.get_public_url.return_value = (
        f"https://storage.example.com/{organization_id}/logo.jpg"
    )

    storage = Mock()
    storage.from_.return_value = bucket

    supabase = Mock()
    supabase.storage = storage

    monkeypatch.setattr(
        "app.modules.organizations.branding.storage.supabase_admin",
        supabase,
    )

    path, url = replace_logo(
        organization_id=organization_id,
        content_type="image/jpeg",
        content=content,
    )

    expected_path = f"{organization_id}/logo.jpg"

    assert path == expected_path
    assert url == f"https://storage.example.com/{expected_path}"

    bucket.upload.assert_called_once_with(
        path=expected_path,
        file=content,
        file_options={
            "content-type": "image/jpeg",
            "upsert": "true",
        },
    )

    bucket.get_public_url.assert_called_once_with(expected_path)


def test_replace_logo_uses_webp_extension_for_webp(monkeypatch):
    organization_id = ORGANIZATION_ID
    content = (
        b"RIFF"
        + b"\x00\x00\x00\x00"
        + b"WEBP"
        + b"webp-content"
    )

    bucket = Mock()
    bucket.get_public_url.return_value = (
        f"https://storage.example.com/{organization_id}/logo.webp"
    )

    storage = Mock()
    storage.from_.return_value = bucket

    supabase = Mock()
    supabase.storage = storage

    monkeypatch.setattr(
        "app.modules.organizations.branding.storage.supabase_admin",
        supabase,
    )

    path, url = replace_logo(
        organization_id=organization_id,
        content_type="image/webp",
        content=content,
    )

    expected_path = f"{organization_id}/logo.webp"

    assert path == expected_path
    assert url == f"https://storage.example.com/{expected_path}"

    bucket.upload.assert_called_once_with(
        path=expected_path,
        file=content,
        file_options={
            "content-type": "image/webp",
            "upsert": "true",
        },
    )

    bucket.get_public_url.assert_called_once_with(expected_path)


# ====================================================================================
# DELETE ORGANIZATION LOGO
# ====================================================================================


def test_delete_logo_removes_expected_storage_path(monkeypatch):
    logo_path = f"{uuid4()}/logo.png"

    bucket = Mock()

    storage = Mock()
    storage.from_.return_value = bucket

    supabase = Mock()
    supabase.storage = storage

    monkeypatch.setattr(
        "app.modules.organizations.branding.storage.supabase_admin",
        supabase,
    )

    delete_logo(logo_path)

    storage.from_.assert_called_once_with(BUCKET)
    bucket.remove.assert_called_once_with([logo_path])