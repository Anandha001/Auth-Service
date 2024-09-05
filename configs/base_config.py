from datetime import timedelta


class BaseConfig(object):
    DB_URI = "postgresql://anandhakannan:admin@localhost/product_fusion"

    ACCESS_TOKEN_EXPIRY_DELTA = timedelta(minutes=45)
    REFRESH_TOKEN_EXPIRY_DELTA = timedelta(days=7)

    SECRET_KEY = "977b5fae4bea7783a845cde8c6e8a8e1a28147befe0040e103d40eaef7c4b1cc"
