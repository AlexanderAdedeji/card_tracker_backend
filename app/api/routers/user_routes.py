from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_201_CREATED,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_400_BAD_REQUEST,
)
from app.api.dependencies.authentication import (
    get_currently_authenticated_user,
    admin_permission_dependency,
)
from app.api.dependencies.db import get_db
from app.core.settings.config import Settings
from app.core.settings.utilities import Utilities
from app.repositories.user_repo import user_repo

from app.schemas.user_schema import UserCreateForm


router = APIRouter()


utils = Utilities()
settings = Settings()


ADMIN_USER = settings.ADMIN_USER
REGULAR_USER = settings.REGULAR_USER


@router.post(
    "/create_user",
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(admin_permission_dependency)],
)
def user_create(
    user_in: UserCreateForm,
    db: Session = Depends(get_db),
    curent_user=Depends(get_currently_authenticated_user),
):
    # return curent_user
    user_exist = user_repo.get_by_email(db, email=user_in.email)
    if user_exist:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=f"User with email {user_in.email} already exist",
        )
    if user_in.role.upper() not in [ADMIN_USER, REGULAR_USER]:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"User role {user_in.role} is not allowed",
        )
    new_user = user_repo.create(db, obj_in=user_in)

    return new_user
