from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_202_ACCEPTED, HTTP_403_FORBIDDEN
from sqlalchemy.orm import Session
from app.api.dependencies.db import get_db
from app.repositories.user_repo import user_repo
from app.core.settings.utilities import Utilities
from app.core.errors import exceptions

from app.schemas.user_schema import UserLogin, UserValidated


router = APIRouter()


utils = Utilities()


@router.post("/log_in")
def log_in(user_login: UserLogin, db: Session = Depends(get_db)):
    user_exist = user_repo.get_by_email(db, email=user_login.email)
    if not user_exist or user_exist.hash_password(user_login.passwword):
        raise exceptions.IncorrectLoginException()
    if not user_exist.is_active:
        raise exceptions.DisallowedLoginException()

    return UserValidated(
        email=user_exist.email,
        first_name=user_exist.first_name,
        last_name=user_exist.last_name,
        role=user_exist.role,
        token=user_exist.generate_jwt(),
    )
