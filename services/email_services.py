import logging
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from uuid import UUID
from configs.base_config import BaseConfig
from fastapi_jwt_auth import AuthJWT
from bs4 import BeautifulSoup
from urllib.parse import urlencode


def send_basic_email_util(
    subject: str,
    html_content: str,
    from_email: str,
    to_emails: list[str],
    cc_emails: list[str] = [],
):
    msg = MIMEMultipart("alternative")
    msg["From"] = from_email
    msg["To"] = ", ".join(to_emails)
    msg["Cc"] = ", ".join(cc_emails)
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))
    recipient_email = to_emails + cc_emails

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(BaseConfig.SENDER_EMAIL, BaseConfig.SENDER_PASSWORD)

        server.sendmail(from_email, recipient_email, msg.as_string())
    except Exception:
        logging.exception("Sending Mail Failed")


def email_sender(
    to_email: str,
    subject: str,
    template: str,
    Authorize: AuthJWT | None = None,
    org_uuid: UUID | None = None,
):
    if template == BaseConfig.VERIFICATION_TEMPLATE:
        html_file_path = "./email_templates/verification.html"
        access_token = Authorize.create_access_token(
            subject=to_email,
            expires_time=BaseConfig.EMAIL_TOKEN_EXPIRY_DELTA,
        )
    elif template == BaseConfig.RESET_PASSWORD_ALERT_TEMPLATE:
        html_file_path = "./email_templates/reset_password.html"
    elif template == BaseConfig.LOGIN_ALERT_TEMPLATE:
        html_file_path = "./email_templates/login_alert.html"

    with open(html_file_path, "r") as html_file:
        soup = BeautifulSoup(html_file.read(), "html.parser")

    targets = soup.find_all("a")

    for v in targets:
        if v["href"] == "verificationlink":
            v["href"] = v["href"].replace(
                "verificationlink",
                f"{BaseConfig.Redirect_URL}auth/onboarding/{org_uuid}?{urlencode({'token': access_token})}",
            )

    return send_basic_email_util(
        subject=subject,
        html_content=str(soup),
        from_email=BaseConfig.SENDER_EMAIL,
        to_emails=[to_email],
    )
