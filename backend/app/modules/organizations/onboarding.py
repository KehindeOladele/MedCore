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
    try:
        organization = get_organization(organization_id)
        organization = getattr(organization, "data", None) if organization is not None else None
        logger.info(f"ORGANIZATION QUERY RESULT: {organization}")
        print(f"organization QUERY RESULT: {organization}")
    except Exception:
        logger.warning(f"organization not found: {organization_id}")
        return

    if not organization:
        logger.warning(f"organization not found or invalid data: {organization_id}")
        return {"status": "not_found"}
    
    
    if organization.get("onboarding_email_sent") and organization.get("onboarding_completed"):
        return

    email = organization.get("email")

    # Email Template context
    context = {
        "organization_name": organization.get("name"),
        "organization_type": organization.get("type"),
        "organization_email": organization.get("email"),
        "admin_email": payload.get("admin_email"),
        "login_url": login_url,
        "support_email": settings.SUPPORT_EMAIL,
        "support_url": settings.FRONTEND_URL + "/login",
        "current_year": datetime.now().year,
    }

    if not email:
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

        html = render_template(
            "welcome_organization.html",
            context
        )

        text = render_template(
            "welcome_organization.txt",
            context,
        )

        # verify end
        logger.info("RENDER TEMPLATE SUCCESS")
        print("RENDER TEMPLATE SUCCESS")

        try:
            email_service = EmailService(
                to=email,
                subject= f"Welcome to MedCore, {organization.get('name')}",
                html=html,
                text=text,
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
            f"Attempting onboarding email to {email}"
        )
        print(f"Attempting onboarding email to {email}")

        # --- send the prepared EmailService instance ---
        response = send_email(email_service)

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

