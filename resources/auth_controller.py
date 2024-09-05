from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from models import get_db
from models.schemas import auth_schemas
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT


from services.member_services import create_member
from services.organisation_services import create_organisation, get_organisation_by_name
from services.user_services import create_user, get_user_by_email
from configs.base_config import BaseConfig

router = APIRouter()


@AuthJWT.load_config
def get_config():
    return auth_schemas.Settings()


@router.post("/signup")
def signup(
    req_body: auth_schemas.AuthBase,
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

    db.commit()
    db.refresh(db_member)
    return {"message": "success", "data": jsonable_encoder(db_member)}


@router.post("/signin")
def signin(
    req_body: auth_schemas.AuthBase,
    db: Session = Depends(get_db),
    authorize: AuthJWT = Depends(),
):
    db_user = get_user_by_email(db=db, email=req_body.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid User")

    if not db_user.verify_password(req_body.password):
        raise HTTPException(status_code=400, detail="Password Mismatch")

    if not db_user.status:
        raise HTTPException(
            status_code=400,
            detail="User not yet active. Please contact your Administrator",
        )

    access_token = authorize.create_access_token(
        subject=db_user.email,
        expires_time=BaseConfig.ACCESS_TOKEN_EXPIRY_DELTA,
    )
    refresh_token = authorize.create_refresh_token(
        subject=db_user.email,
        expires_time=BaseConfig.REFRESH_TOKEN_EXPIRY_DELTA,
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
