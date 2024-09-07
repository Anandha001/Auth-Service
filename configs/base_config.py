from datetime import timedelta


class BaseConfig(object):
    DB_URI = "postgresql://anandhakannan:admin@localhost/product_fusion"

    ACCESS_TOKEN_EXPIRY_DELTA = timedelta(minutes=45)
    REFRESH_TOKEN_EXPIRY_DELTA = timedelta(days=7)
    EMAIL_TOKEN_EXPIRY_DELTA = timedelta(minutes=1440)

    SECRET_KEY = "977b5fae4bea7783a845cde8c6e8a8e1a28147befe0040e103d40eaef7c4b1cc"

    SENDER_EMAIL = "Replace with your gmass id"
    SENDER_PASSWORD = "Replace with your gmass password"

    VERIFICATION_TEMPLATE = "Verification"
    RESET_PASSWORD_ALERT_TEMPLATE = "ResetPasswordAlert"
    LOGIN_ALERT_TEMPLATE = "LoginAlert"

    Redirect_URL = "http://localhost:8000/api/v1/"
