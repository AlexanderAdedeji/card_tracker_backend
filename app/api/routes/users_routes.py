from typing import List, Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user_schema import (
    ResetUserPassword,
    UserCreate,
    User,
    UserValidated,
    UserLogin,
)
from app.schemas import card_schema, token_schema, user_schema
from app.models import user_model
from app.api.dependencies.authentication import auth
from app.repositories.user_repo import user_repo

from app.api.dependencies.db.db import get_db
from sqlalchemy import func
from app.core.settings.utilities import Utilities

router = APIRouter()


@router.post("/create_users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_exist = user_repo.get_by_email(db, email=user.email)
    if user_exist:
        raise HTTPException(status_code=403, detail="this email already exists")
    new_user = user_repo.create(db, obj_in=user)
    return User(
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
    )


@router.post("/login")
def user_login(login: UserLogin, db: Session = Depends(get_db)):
    user = user_repo.get_by_email(db, email=login.email)
    if not user:
        raise HTTPException(status_code=404, detail=f"Invalid Login Credentials")
    is_password = Utilities.verify_password(login.password, user.hashed_password)
    if not is_password:
        raise HTTPException(status_code=403, detail=f"Invalid Login Credentials")
    if not user.is_active:
        raise HTTPException(status_code=403, detail=f"Account not active")

    return UserValidated(
        first_name=user.first_name,
        last_name=user.last_name,
        token=user.generate_jwt(),
        isPasswordReset=user.password_reset,
    )


@router.put(
    "/deactivateUser",
    #  dependencies=[Depends(superuser_and_admin_permission)]
)
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    user_exist = user_repo.get(db, id=user_id)
    if not user_exist:
        raise HTTPException(status_code=403, detail="This user does not exist")
    if user_exist.first_name.lower() == "super":
        raise HTTPException(status_code=403, detail="This user cannot be deactivated")
    if not user_exist.is_active:
        raise HTTPException(
            status_code=403, detail="This user has already been  deactivated"
        )

    user_deactiavted = user_repo.deactivate(db, db_obj=user_exist)

    return {
        "message": f"{user_deactiavted.first_name} {user_deactiavted.first_name} has been deactivated Successfully"
    }


@router.put(
    "/activateUser",
    # dependencies=[
    #     Depends(superuser_and_admin_permission),
    # ],
)
def activate_user(user_id: int, db: Session = Depends(get_db)):
    user_exist = user_repo.get(db, id=user_id)
    if not user_exist:
        raise HTTPException(status_code=403, detail="This user does not exist")
    if user_exist.is_active:
        raise HTTPException(
            status_code=403, detail="This user has already been activated"
        )

    user_actiavted = user_repo.activate(db, db_obj=user_exist)
    return {
        "message": f"{user_actiavted.first_name} {user_actiavted.first_name} has been activated Successfully"
    }


@router.put(
    "/reset_password",
)
def reset_password(password_detail: ResetUserPassword, db: Session = Depends(get_db)):
    user_exist = user_repo.get(db, id=password_detail.id)
    if not user_exist:
        raise HTTPException(status_code=403, detail="This user does not exist")
    user_repo.reset_password(
        db, db_obj=user_exist, new_password=password_detail.passwordStr
    )
    print(password_detail.passwordStr)
    user_repo.set_password_reset_check(db, db_obj=user_exist, status=True)
    return {"message": "User password reset successfully"}


# @router.put("/change_password")
# def change_password(
#     new_password: str,
#     current_user: User = Depends(auth.get_currently_authenticated_user),
#     db: Session = Depends(get_db),
# ):
#     user = user_repo.get(db, id=current_user.id)
#     user_type = user_type_repo.get(db, id=user.user_type_id)
#     user_repo.reset_password(db, db_obj=user, new_password=new_password)
#     user_reset = user_repo.set_password_reset_check(db, db_obj=user, status=False)
#     print(user_reset.password_reset)
#     if user_type.name.lower() == "editor":
#         imagesToUpload = (
#             db.query(ImageStatus).filter(ImageStatus.edited_by == user.id).count()
#         )
#         return UserValidated(
#             id=user_reset.id,
#             first_name=user_reset.first_name,
#             last_name=user_reset.last_name,
#             user_type=user_type.name,
#             uploadImageCount=imagesToUpload,
#             token=user_reset.generate_jwt(),
#             isPasswordReset=user_reset.password_reset,
#         )
#     else:
#         return UserValidated(
#             first_name=user_reset.first_name,
#             last_name=user_reset.last_name,
#             user_type=user_type.name,
#             token=user_reset.generate_jwt(),
#             isPasswordReset=user_reset.password_reset,
#         )




@router.get("/get_all_visits")
def get_all_visits(db:Session = Depends(get_db)):
    return 'All visits'