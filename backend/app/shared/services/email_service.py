import resend
from app.core.config import settings
from app.shared.schemas.email_service import EmailService


# ----- Initial Resend API -----
resend.api_key = settings.RESEND_API_KEY


# ----- Send Email Service -----
def send_email(email_service: EmailService):

    return resend.Emails.send({
        "from": settings.EMAIL_FROM,
        "to": [email_service.to],
        "subject": email_service.subject,
        "html": email_service.html
    })