from fastapi import FastAPI, APIRouter as global_router
from starlette.middleware.cors import CORSMiddleware
import starlette.responses as _responses


origins = ["*"]


def create_application_instance() -> FastAPI:
    application = FastAPI(title="Public Card Tracking API")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # application.include_router(global_router, prefix="/public_card_tracking_api")
    return application


app = create_application_instance()


@app.get("/")
async def root():
    return _responses.RedirectResponse("/docs")
