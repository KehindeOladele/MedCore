"""Supabase Storage operations isolated from branding business rules."""

from uuid import UUID

from app.core.supabase_admin import supabase_admin

from .constants import ALLOWED_LOGO_CONTENT_TYPES, BUCKET, MAX_LOGO_SIZE_BYTES
from .exceptions import InvalidLogoError


def validate_logo(content_type: str | None, content: bytes) -> str:
    """Return the trusted extension after applying the upload safety policy."""
    if content_type not in ALLOWED_LOGO_CONTENT_TYPES or not content or len(content) > MAX_LOGO_SIZE_BYTES:
        raise InvalidLogoError()
    signatures = {
        "image/png": content.startswith(b"\x89PNG\r\n\x1a\n"),
        "image/jpeg": content.startswith(b"\xff\xd8\xff"),
        "image/webp": content.startswith(b"RIFF") and content[8:12] == b"WEBP",
    }
    if not signatures[content_type]:
        raise InvalidLogoError()
    return ALLOWED_LOGO_CONTENT_TYPES[content_type]


def replace_logo(*, organization_id: UUID, content_type: str, content: bytes) -> tuple[str, str]:
    """Store a deterministic per-organization logo and return its path and URL."""
    extension = validate_logo(content_type, content)
    path = f"{organization_id}/logo.{extension}"
    bucket = supabase_admin.storage.from_(BUCKET)
    bucket.upload(path=path, file=content, file_options={"content-type": content_type, "upsert": "true"})
    return path, bucket.get_public_url(path)


def delete_logo(path: str) -> None:
    """Delete the internally stored path; this never accepts a public URL."""
    supabase_admin.storage.from_(BUCKET).remove([path])
