from pydantic import (
    BaseModel, 
    ConfigDict, 
    Field, 
    field_validator, 
    model_validator
)


HEX_COLOR_PATTERN = r"^#[0-9A-Fa-f]{6}$"

# -----------------------------------------------------------------------------------
# BRANDING SCHEMAS
# -----------------------------------------------------------------------------------
class BrandingThemeUpdate(BaseModel):
    """A small, portable visual theme for patient- and staff-facing clients."""

    primary_color: str | None = Field(default=None, pattern=HEX_COLOR_PATTERN)
    secondary_color: str | None = Field(default=None, pattern=HEX_COLOR_PATTERN)

    @model_validator(mode="after")
    def require_a_changed_field(self):
        if not self.model_fields_set:
            raise ValueError("Provide primary_color or secondary_color.")
        return self

    @field_validator("primary_color", "secondary_color")
    @classmethod
    def normalize_color(cls, value: str | None) -> str | None:
        return value.upper() if value else value

# -----------------------------------------------------------------------------------
# BRANDING RESPONSE SCHEMA
# -----------------------------------------------------------------------------------
class BrandingResponse(BaseModel):
    organization_id: str
    logo_url: str | None = None
    primary_color: str | None = None
    secondary_color: str | None = None

    model_config = ConfigDict(from_attributes=True)
