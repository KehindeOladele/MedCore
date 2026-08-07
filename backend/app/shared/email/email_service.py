import resend
from typing import cast

from app.core.config import settings
from app.shared.schemas.email_service import EmailService


# ----- Initial Resend API -----
resend.api_key = settings.RESEND_API_KEY


# ----- Send Email Service -----
def send_email(email_service: EmailService):

    print("EMAIL SEND START")
    print("TO:", email_service.to)
    print("FROM:", settings.EMAIL_FROM)

    if not email_service.to:
        raise ValueError("Missing recipient")

    if not email_service.subject:
        raise ValueError("Missing subject")

    if not email_service.html:
        raise ValueError("Missing HTML body")

    # Ensure values are plain strings (Resend types expect str, not EmailStr | None)
    params = cast(resend.Emails.SendParams, {
        "from": str(settings.EMAIL_FROM),
        "to": [str(email_service.to)],
        "subject": str(email_service.subject),
        "html": str(email_service.html),
    })

    print("RESEND PARAMS:", params)

    response = resend.Emails.send(params)

    print("RESEND RESPONSE:", response)

    if not response:
        raise RuntimeError("Resend returned no response")

    return response