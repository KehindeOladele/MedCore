from app.modules.organizations.profile.schemas import (
    OrganizationProfileUpdate,
)


# -------------------------------
# SCHEMA TESTS
# -------------------------------
def test_profile_update_schema():

    payload = OrganizationProfileUpdate(
        name="MedCore Hospital",
        telecom={
            "phone": "+2348000000000",
            "email": "admin@medcore.com",
            "website": "https://medcore.com",
        },
        address={
            "line": "1 Health Avenue",
            "city": "Ikeja",
            "state": "Lagos",
            "postal_code": "100001",
            "country": "Nigeria",
        },
    )

    assert payload.name == "MedCore Hospital"
    assert payload.telecom.phone == "+2348000000000"
    assert payload.address.city == "Ikeja"