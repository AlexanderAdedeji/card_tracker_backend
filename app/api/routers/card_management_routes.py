from fastapi import APIRouter




router = APIRouter()




@router.get("/")
def search_card(lasrra_id:str):
    return lasrra_id