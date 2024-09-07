from models.schemas.common import BaseModel
from configs.base_config import BaseConfig


class AuthBase(BaseModel):
    email: str
    password: str


class RegisterUser(AuthBase):
    organisation_name: str


class Settings(BaseModel):
    authjwt_secret_key: str = BaseConfig.SECRET_KEY
