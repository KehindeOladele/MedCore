from app.core.audit.actions import AuditActions
from app.core.audit.service import log_audit_event
from app.core.supabase_admin import supabase_admin
from app.core.config import settings
from app.shared.email.email_service import send_email
from app.shared.services.template_service import render_template
from app.shared.schemas.email_service import EmailService
from datetime import datetime, timezone
from pydantic import ValidationError
from app.modules.organizations.exceptions import (
    EmailDeliveryError,
    InvalidOrganizationEmailError
)
from app.modules.organizations.queries import get_organization
import logging
import traceback

logger = logging.getLogger(__name__)


# -----------------------------------------
# Onboarding organization Email Serivice 
# -----------------------------------------
def send_organization_onboarding_email(
        organization_id: str,
        payload: dict
        ):

    logger.info(
        f"ONBOARDING STARTED FOR {organization_id}"
    )
    print(
        f"ONBOARDING STARTED FOR {organization_id}"
    )

    # Get and check if organizaition

    organization = get_organization(organization_id)
    logger.info(f"ORGANIZATION QUERY RESULT: {organization}")
    print(f"organization QUERY RESULT: {organization}")

    if organization.get("onboarding_email_sent") and organization.get("onboarding_completed"):
        logger.info(
            "Organization %s already onboarded.",
            organization_id
        )
        return

    # Email Template context
    context = {
        "organization_name": organization.get("name"),
        "organization_type": organization.get("type"),
        "organization_email": organization.get("email"),
        "admin_email": payload.get("admin_email"),
        "login_url": settings.FRONTEND_URL + "/login",
        "support_email": settings.SUPPORT_EMAIL,
        "support_email": settings.SUPPORT_EMAIL,
        "current_year": datetime.now().year,
    }

    # Get and check for Recipient email
    recipient = (
        payload.get("admin_email")
        or organization.get("email")
    )

    if not recipient:
        raise InvalidOrganizationEmailError(
            f"Organization {organization_id} has no email address."
        )
    
    # Onboarding status as processing before rendering template
    (
        supabase_admin
        .table("organizations")
        .update({
            "onboarding_status": "processing",
            "onboarding_last_attempt_at": datetime.now(timezone.utc).isoformat()
        })
        .eq("id", organization_id)
        .execute()
    )

    try:
        #  verify start
        logger.info("RENDER TEMPLATE START")
        print("RENDER TEMPLATE START")

        # Render html template
        html = render_template(
            "welcome_organization.html",
            context
        )

        # verify end
        logger.info("RENDER TEMPLATE SUCCESS")
        print("RENDER TEMPLATE SUCCESS")

        try:
            email_service = EmailService(
                to=recipient,
                subject= f"Welcome to MedCore, {organization.get('name')}",
                html=html,
            )
            
        except (ValidationError, TypeError) as ve:
            logger.warning(f"Invalid organization email for {organization_id}: {email}")

            # Onboarding status Processig after rending for in invalid email
            (
                supabase_admin
                .table("organizations")
                .update({
                    "onboarding_last_error": str(ve),
                    "onboarding_failure_reason": "invalid_email",
                    "onboarding_retry_count": int(organization.get("onboarding_retry_count") or 0) + 1,
                    "onboarding_status": "processing",
                    "onboarding_last_attempt_at": datetime.now(timezone.utc).isoformat()
                })
                .eq("id", organization_id)
                .execute()
            )
            return {"status": "invalid_email"}
        
        # log and print onboarding email
        logger.info(
            f"Attempting onboarding email to {recipient}"
        )
        print(f"Attempting onboarding email to {recipient}")

        # --- send the prepared EmailService instance ---
        response = send_email(email_service)

        logger.info("EMAIL RESPONSE TYPE: %s", type(response))
        logger.info("EMAIL RESPONSE: %r", response)

        print("EMAIL RESPONSE TYPE:", type(response))
        print("EMAIL RESPONSE:", repr(response))

        # log and print response
        log_audit_event(
            actor_id=organization_id,
            actor_type="organization",
            action=AuditActions.ONBOARDING_EMAIL_SENT,
            resource_type="organization",
            resource_id=organization_id
        )

        logger.info(
            f"Resend response: {response}"
        )
        print(f"Resend response: {response}")

        if not response:
            raise EmailDeliveryError("Email send failed")
        
        now = datetime.now(timezone.utc).isoformat()

        # Onboarding status as Completed 
        (
            supabase_admin
            .table("organizations")
            .update({
                "onboarding_email_sent": True,
                "onboarding_email_sent_at": now,
                "onboarding_retry_count": 0,
                "onboarding_last_error": None,
                "onboarding_status": "completed",
                "onboarding_completed": True,
                "onboarding_completed_at": now
            })
            .eq("id", organization_id)
            .execute()
        )

        logger.info(
            "ONBOARDING CALL STACK:\n%s",
            "".join(traceback.format_stack())
        )

    except Exception as e:
        logger.exception(
            f"Failed loading organization {organization_id}: {str(e)}"
        )

        #  Onboarding status as failed
        (
            supabase_admin
            .table("organizations")
            .update({
                "onboarding_last_error": str(e),
                "onboarding_failure_reason": "email_delivery_failed",
                "onboarding_retry_count": int(organization.get("onboarding_retry_count") or 0) + 1,
                "onboarding_status": "failed",
                "onboarding_last_attempt_at": datetime.now(timezone.utc).isoformat()
            })
            .eq("id", organization_id)
            .execute()
        )

        raise

