from fastapi import Depends, FastAPI, status, HTTPException, Request, APIRouter as global_router
from app.api.routes.routes import router as global_router
from fastapi.middleware.cors import CORSMiddleware
from app.databases.session import engine, Base
from app.commonLib.models import Base
Base.metadata.create_all(bind=engine)

origins= ["*"]


def create_application_instance()-> FastAPI:
    application= FastAPI(title="Public Card Tracking API", DEBUG=True)
    application.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )
    application.include_router(global_router, prefix= "/public_card_tracking_api")
    return application
app= create_application_instance()








@app.get('/')
async def root():
    return _responses.RedirectResponse("/docs")


