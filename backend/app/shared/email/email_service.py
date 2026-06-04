import resend
from app.core.config import settings
from app.shared.schemas.email_service import EmailService


# ----- Initial Resend API -----
resend.api_key = settings.RESEND_API_KEY


# ----- Send Email Service -----
def send_email(email_service: EmailService):
    try:
        # Build params excluding None values to satisfy strict typing for resend.SendParams
        if email_service.to is None or email_service.subject is None:
            raise ValueError("Email destination and subject are required")

        params: resend.Emails.SendParams = {
            "from": str(settings.EMAIL_FROM),
            "to": [str(email_service.to)],
            "subject": str(email_service.subject),
            "reply_to": str(settings.EMAIL_REPLY_TO)
        }

        if getattr(email_service, "html", None) is not None:
            params["html"] = email_service.html

        return resend.Emails.send(params)
    except Exception as e:
        raise Exception(
            f"Email delivery failed: {str(e)}"
        )