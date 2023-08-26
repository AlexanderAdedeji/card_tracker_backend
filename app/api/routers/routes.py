from fastapi import APIRouter
from app.api.routers import card_management

router = APIRouter()


router.include_router(card_management.router, tags=['Card Management'], prefix="/card-management")


