from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

from app.modules.organizations.exceptions import (
    OrganizationError,
    UserOrganizationNotFoundError,
    OrganizationNotFoundError,
    OrganizationAccessDeniedError,
    OrganizationMembershipRequiredError,
    OrganizationAdminRequiredError,
    OrganizationProfileValidationError,
    OrganizationProfileUpdateError,
    InvalidOrganizationEmailError,
    EmailDeliveryError,
)


# ----------------------------
# Generic Organization Handler
# ----------------------------
async def organization_error_handler(
    request: Request,
    exc: OrganizationError,
):
    """
    Fallback handler for organization domain errors.
    """

    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc),
        },
    )


# ------------------------------
# Organization Not Found Handler
# ------------------------------
async def organization_not_found_handler(
    request: Request,
    exc: OrganizationNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc),
        },
    )


# -----------------------------------
# User Organization Not Found Handler
# -----------------------------------
async def user_organization_not_found_handler(
    request: Request,
    exc: UserOrganizationNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc),
        },
    )


# -------------------------------------
# Organization Access Forbidden Handler
# -------------------------------------
async def organization_access_denied_handler(
    request: Request,
    exc: OrganizationAccessDeniedError,
):
    return JSONResponse(
        status_code=403,
        content={
            "detail": str(exc),
        },
    )


# -------------------------------------
# Membership Required Handler
# -------------------------------------
async def organization_membership_required_handler(
    request: Request,
    exc: OrganizationMembershipRequiredError,
):
    return JSONResponse(
        status_code=403,
        content={
            "detail": str(exc),
        },
    )


# -------------------------------------
# Admin Required Handler
# -------------------------------------
async def organization_admin_required_handler(
    request: Request,
    exc: OrganizationAdminRequiredError,
):
    return JSONResponse(
        status_code=403,
        content={
            "detail": str(exc),
        },
    )


# -------------------------------------
# Profile Validation Handler
# -------------------------------------
async def organization_profile_validation_handler(
    request: Request,
    exc: OrganizationProfileValidationError,
):
    return JSONResponse(
        status_code=422,
        content={
            "detail": str(exc),
        },
    )


# -------------------------------------
# Update Failure Handler
# -------------------------------------
async def organization_profile_update_handler(
    request: Request,
    exc: OrganizationProfileUpdateError,
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": str(exc),
        },
    )


# -------------------------------------
# Invalid Email Handler
# -------------------------------------
async def invalid_organization_email_handler(
    request: Request,
    exc: InvalidOrganizationEmailError,
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc),
        },
    )


# -------------------------------------
# Email Delivery Failure Handler
# -------------------------------------
async def email_delivery_handler(
    request: Request,
    exc: EmailDeliveryError,
):
    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
        },
    )


# -------------------------------------
# Register Exception Handlers
# -------------------------------------
def register_exception_handlers(
    app: FastAPI,
) -> None:
    """
    Register all application exception handlers.

    This serves as the central registration point for
    translating domain exceptions into HTTP responses.
    """

    # -------------------------
    # Organization Exceptions
    # -------------------------
    app.add_exception_handler(
        OrganizationError,
        organization_error_handler,
    )

    app.add_exception_handler(
        UserOrganizationNotFoundError,
        user_organization_not_found_handler,
    )

    app.add_exception_handler(
        OrganizationNotFoundError,
        organization_not_found_handler,
    )

    app.add_exception_handler(
        OrganizationAccessDeniedError,
        organization_access_denied_handler,
    )

    app.add_exception_handler(
        OrganizationMembershipRequiredError,
        organization_membership_required_handler,
    )

    app.add_exception_handler(
        OrganizationAdminRequiredError,
        organization_admin_required_handler,
    )

    app.add_exception_handler(
        OrganizationProfileValidationError,
        organization_profile_validation_handler,
    )

    app.add_exception_handler(
        OrganizationProfileUpdateError,
        organization_profile_update_handler,
    )

    app.add_exception_handler(
        InvalidOrganizationEmailError,
        invalid_organization_email_handler,
    )

    app.add_exception_handler(
        EmailDeliveryError,
        email_delivery_handler,
    )


    # ======================================
    # Departments
    # ======================================
    ...

    # ======================================
    # Healthcare Services
    # ======================================
    ...

    # ======================================
    # Practitioners
    # ======================================
    ...

    # ======================================
    # Patients
    # ======================================
    ...

    # ======================================
    # Appointments
    # ======================================
    ...