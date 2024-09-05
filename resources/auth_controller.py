from fastapi import APIRouter, Depends, HTTPException
from models import get_db
from models.schemas import auth_schemas
from sqlalchemy.orm import Session

from services.member_services import create_member
from services.organisation_services import create_organisation, get_organisation_by_name
from services.user_services import create_user, get_user_by_email

router = APIRouter()


@router.post("/signup")
def signup(
    req_body: auth_schemas.RegisterUser,
    db: Session = Depends(get_db),
):
    db_user = get_user_by_email(db=db, email=req_body.email)
    if db_user:
        raise HTTPException(status_code=400, detail="email already registered")

    db_user = create_user(db=db, email=req_body.email, password=req_body.password)

    db_organisation = get_organisation_by_name(db=db, name=req_body.organisation_name)
    if not db_organisation:
        db_organisation = create_organisation(db=db, name=req_body.organisation_name)

    db_member = create_member(
        db=db, org_uuid=db_organisation.uuid, user_uuid=db_user.uuid
    )

    return {"message": "success", "data": db_member}
