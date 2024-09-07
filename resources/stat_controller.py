from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session
import pandas as pd
from models import get_db, models

router = APIRouter()


@router.get("/role_wise_users")
def get_role_wise_users(db: Session = Depends(get_db)):
    TERMS = [
        models.Role.name.label("Role Name"),
        func.count(models.Member.uuid).label("User count"),
    ]
    query = (
        select(*TERMS)
        .outerjoin(models.Member, models.Member.role_uuid == models.Role.uuid)
        .group_by(models.Role.name)
    )
    df = pd.read_sql(query, db.get_bind())
    result = df.to_dict(orient="records")

    return {"message": "success", "data": result}


@router.get("/organization_wise_members")
def get_organization_wise_members(db: Session = Depends(get_db)):
    TERMS = [
        models.Organisation.name.label("Organisation Name"),
        func.count(models.Member.uuid).label("Member count"),
    ]
    query = (
        select(*TERMS)
        .outerjoin(models.Member, models.Member.org_uuid == models.Organisation.uuid)
        .group_by(models.Organisation.name)
    )
    df = pd.read_sql(query, db.get_bind())
    result = df.to_dict(orient="records")

    return {"message": "success", "data": result}


@router.get("organization_role_wise_users")
def get_organization_role_wise_users(db: Session = Depends(get_db)):
    TERMS = [
        models.Organisation.name.label("Organisation Name"),
        models.Role.name.label("Role Name"),
        func.count(models.Member.uuid).label("Member count"),
    ]
    query = (
        select(*TERMS)
        .join(models.Member, models.Member.org_uuid == models.Organisation.uuid)
        .join(models.Role, models.Member.role_uuid == models.Role.uuid)
        .group_by(models.Organisation.name, models.Role.name)
    )
    df = pd.read_sql(query, db.get_bind())
    result = df.to_dict(orient="records")

    return {"message": "success", "data": result}
