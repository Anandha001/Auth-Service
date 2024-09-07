from models.enums import Role
from models.schemas.common import BaseModel


class MemberBase(BaseModel):
    email: str
    organisation_name: str
    role_name: Role
