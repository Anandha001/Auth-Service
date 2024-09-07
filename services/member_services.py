from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import models
from models.enums import Role
from services import ROLE_DESCRIPTION
from services.role_services import create_role, get_role_by_name


def create_member(
    db: Session, org_uuid: UUID, user_uuid: UUID, role_name: str | None = Role.OWNER
) -> models.Member:
    db_role = get_role_by_name(db=db, name=role_name, org_uuid=org_uuid)
    if not db_role:
        db_role = create_role(
            db=db,
            name=role_name,
            description=ROLE_DESCRIPTION[role_name],
            org_uuid=org_uuid,
        )

    db_member = make_member(
        db=db, org_uuid=org_uuid, user_uuid=user_uuid, role_uuid=db_role.uuid
    )
    return db_member


def make_member(
    db: Session, org_uuid: UUID, user_uuid: UUID, role_uuid: UUID
) -> models.Member:
    db_member = get_member(
        db=db, org_uuid=org_uuid, user_uuid=user_uuid, role_uuid=role_uuid
    )
    if db_member and db_member.status:
        raise HTTPException(status_code=400, detail="Member already registered")

    if not db_member:
        db_member = models.Member(
            org_uuid=org_uuid,
            user_uuid=user_uuid,
            role_uuid=role_uuid,
        )
        db.add(db_member)
        db.flush()
        db.refresh(db_member)

    return db_member


def get_member(
    db: Session, org_uuid: UUID, user_uuid: UUID, role_uuid: UUID
) -> models.Member:
    db_member = db.scalars(
        select(models.Member).where(
            models.Member.org_uuid == org_uuid,
            models.Member.user_uuid == user_uuid,
            models.Member.role_uuid == role_uuid,
        )
    ).first()
    return db_member
