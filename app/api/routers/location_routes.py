from fastapi import APIRouter

router = APIRouter()



@router.get("/location")
def location():
    return {"message": "Location"}