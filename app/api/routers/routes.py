from fastapi import APIRouter
from app.api.routers import card_management_routes, location_routes

router = APIRouter()


router.include_router(card_management_routes.router, tags=['Card Management'], prefix="/card_management")
router.include_router(location_routes.router, tags=['Location'], prefix="/location")

