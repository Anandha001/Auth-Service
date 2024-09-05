from uuid import UUID
from sqlalchemy.orm import Session
from models import models
from models.enums import Role, RoleDescription
from services.role_services import create_role, get_role_by_name


def create_member(db: Session, org_uuid: UUID, user_uuid: UUID) -> models.Member:
    db_role = get_role_by_name(db=db, name=Role.OWNER, org_uuid=org_uuid)
    if not db_role:
        db_role = create_role(
            db=db,
            name=Role.OWNER,
            description=RoleDescription.OWNER,
            org_uuid=org_uuid,
        )
    db_member = models.Member(
        org_uuid=org_uuid,
        user_uuid=user_uuid,
        role_uuid=db_role.uuid,
        status=1,
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member
