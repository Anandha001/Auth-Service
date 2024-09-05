from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import models


def get_role_by_name(db: Session, name: str, org_uuid: UUID) -> models.Role:
    db_role = db.scalars(
        select(models.Role).where(
            models.Role.name == name, models.Role.org_uuid == org_uuid
        )
    ).first()
    return db_role


def create_role(
    db: Session, name: str, description: str, org_uuid: UUID
) -> models.Role:
    db_role = models.Role(
        name=name,
        description=description,
        status=1,
        org_uuid=org_uuid,
    )
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role
