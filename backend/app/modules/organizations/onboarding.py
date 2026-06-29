from datetime import datetime, timezone
from app.core.supabase_admin import supabase_admin
from app.shared.email.email_service import send_email
from app.shared.services.template_service import render_template
from app.shared.schemas.email_service import EmailService
from pydantic import ValidationError
from app.modules.organizations.exceptions import EmailDeliveryError
from app.core.audit.service import log_audit_event
from app.core.audit.actions import AuditActions
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

    try:
        result = (
            supabase_admin
            .table("organizations")
            .select("*")
            .eq("id", organization_id)
            .maybe_single()
            .execute()
        )
        organization = getattr(result, "data", None) if result is not None else None
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

    if not email:
        return {"status": "missing_email"}

    try:
        #  verify start
        logger.info("RENDER TEMPLATE START")
        print("RENDER TEMPLATE START")

        html = render_template(
            "welcome_organization.html",
            {
                "first_name": organization.get("first_name"),
                "medical_id": organization.get("medical_id")
            }
        )

        # verify end
        logger.info("RENDER TEMPLATE SUCCESS")
        print("RENDER TEMPLATE SUCCESS")

        try:
            email_service = EmailService(
            to=email,
            subject="Welcome to MedCore",
            html=html
        )
        except (ValidationError, TypeError) as ve:
            logger.warning(f"Invalid organization email for {organization_id}: {email}")
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

        # send the prepared EmailService instance
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

