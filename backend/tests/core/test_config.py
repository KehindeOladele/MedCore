from app.core.config import Settings


#==========================================================
# FHIR CONFIGURATION TESTS
# =========================================================
def test_fhir_version_defaults_to_r4():
    settings = Settings()

    assert settings.FHIR_VERSION == "R4"


def test_fhir_base_url_defaults_to_none():
    settings = Settings()

    assert settings.FHIR_BASE_URL is None