from enum import StrEnum


class Role(StrEnum):
    OWNER = "owner"


class RoleDescription(StrEnum):
    OWNER = "full administrative control over an organization"
