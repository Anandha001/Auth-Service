from sqlalchemy import select
from sqlalchemy.orm import Session
from models import models


def get_organisation_by_name(db: Session, name: str) -> models.Organisation:
    db_organisation = db.scalars(
        select(models.Organisation).where(models.Organisation.name == name)
    ).first()
    return db_organisation


def create_organisation(db: Session, name: str) -> models.Organisation:
    db_organisation = models.Organisation(name=name, status=1)
    db.add(db_organisation)
    db.flush()
    db.refresh(db_organisation)
    return db_organisation
