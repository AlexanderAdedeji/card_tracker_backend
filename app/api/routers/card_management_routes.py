from fastapi import APIRouter, Depends, Request, HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from sqlalchemy.orm import Session
from app.repositories.search_log_repo import search_log_repo
from app.api.dependencies.db import get_db
from app.schemas.search_log_schemas import SearchLogBase


router = APIRouter()


@router.get("/search/{lasrra_id}")
async def visitor_get_status(
    request: Request, lasrra_id: str, db: Session = Depends(get_db)
):
    search_limit_exceeded = search_log_repo.check_ip_search_limit(
        db, ip=request.client.host
    )

    if search_limit_exceeded:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="You have excceded your search limit for the day",
        )
    search_in = SearchLogBase(ip_address=request.client.host, lasrra_id=lasrra_id)
    search_log_repo.create(db, obj_in=search_in)
    return lasrra_id
