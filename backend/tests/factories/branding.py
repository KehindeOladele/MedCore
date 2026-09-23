from copy import deepcopy
from app.modules.organizations.branding.schemas import BrandingResponse
from tests.factories.constants import ORGANIZATION_ID
from app.modules.organizations.branding import router


# ====================================================================================
# TEST FACTORIES
# ====================================================================================
_DEFAULT_BRANDING_ROW = {
        "organization_id": str(ORGANIZATION_ID),
        "logo_url": "https://example.com/logo.png",
        "primary_color": "#FFFFFF",
        "secondary_color": "#000000",
    }

def branding_response(**overrides):
    branding_response= deepcopy(_DEFAULT_BRANDING_ROW)
    branding_response.update(overrides)

    return BrandingResponse(**branding_response)