import pytest

from app.modules.organizations.branding.constants import (
    MAX_LOGO_SIZE_BYTES,
)
from app.modules.organizations.branding.exceptions import InvalidLogoError
from app.modules.organizations.branding.storage import validate_logo


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