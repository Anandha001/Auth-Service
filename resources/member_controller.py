from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete, update
from models import get_db, models
from models.schemas import member_schemas
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT


from services.email_services import email_sender
from services.member_services import create_member
from services.organisation_services import get_organisation_by_name
from services.user_services import get_user_by_email
from configs.base_config import BaseConfig

router = APIRouter()


@router.post("/invite_member")
def invite_member(
    req_body: member_schemas.MemberBase,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    db_user = get_user_by_email(db=db, email=req_body.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid User")

    db_organisation = get_organisation_by_name(db=db, name=req_body.organisation_name)
    if not db_organisation:
        raise HTTPException(status_code=400, detail="Invalid Organisation")

    db_member = create_member(
        db=db,
        org_uuid=db_organisation.uuid,
        user_uuid=db_user.uuid,
        role_name=req_body.role_name,
    )
    db.commit()
    db.refresh(db_member)

    email_sender(
        db_user.email,
        "Verification Email",
        BaseConfig.VERIFICATION_TEMPLATE,
        Authorize,
        db_organisation.uuid,
    )

    return {"message": "success", "data": jsonable_encoder(db_member)}


@router.delete("")
def delete_member(member_uuid: UUID, db: Session = Depends(get_db)):
    db.execute(delete(models.Member).where(models.Member.uuid == member_uuid))
    db.commit()
    return {"message": "member deleted sucessfully"}


@router.patch("/update_role")
def update_member_role(
    member_uuid: UUID, role_uuid: UUID, db: Session = Depends(get_db)
):
    db.execute(
        update(models.Member)
        .where(models.Member.uuid == member_uuid)
        .values(role_uuid=role_uuid)
    )
    db.commit()
    return {"message": "member role updated sucessfully"}
