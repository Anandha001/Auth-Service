from models.schemas.common import BaseModel


class RegisterUser(BaseModel):
    email: str
    password: str
    organisation_name: str
