from app.api.routes import users_routes,location_routes,visitor_routes
from fastapi import APIRouter


router = APIRouter()


router.include_router(users_routes.router, prefix="/users",
    tags=['Users'])
router.include_router(visitor_routes.router,  prefix="/visitor",
    tags=['Guest'])
router.include_router(location_routes.router, prefix="/location", tags=['Location'])