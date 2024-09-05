from sqlalchemy import select
from sqlalchemy.orm import Session
from models import models


def get_user_by_email(db: Session, email: str) -> models.User:
    db_user = db.scalars(select(models.User).where(models.User.email == email)).first()
    return db_user


def create_user(db: Session, email: str, password: str) -> models.User:
    db_user = models.User(email=email.lower(), status=1)
    db_user.hash_password(password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
