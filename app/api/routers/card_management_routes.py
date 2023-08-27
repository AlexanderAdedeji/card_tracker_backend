from fastapi import APIRouter, Depends, Request, HTTPException
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from sqlalchemy.orm import Session
from app.commonLib.lasrra_api import LasrraAPI
from app.models.collection_centers_models import CollectionCentre
from app.models.local_goverment_models import LocalGovernment
from app.repositories.search_log_repo import search_log_repo
from app.api.dependencies.db import get_db
from app.schemas.card_management_schema import (
    CardInfo,
    DeliverCard,
    OTPRequest,
    RelocateCard,
    VerifyOTP,
)
from app.schemas.search_log_schemas import SearchLogBase


router = APIRouter()

lasrra_api = LasrraAPI()


def check_if_data(data):
    return "N/A" if data == None else data


def check_card_is_delivered(data):
    data = check_if_data(data)
    return True if "delivered" in data.lower() else False


@router.get("/search/{lasrra_id}")
async def visitor_get_status(
    request: Request, lasrra_id: str, db: Session = Depends(get_db)
):
    search_limit_exceeded = search_log_repo.check_ip_search_limit(
        db, ip=request.client.host
    )

    # if search_limit_exceeded:
    #     raise HTTPException(
    #         status_code=HTTP_403_FORBIDDEN,
    #         detail="You have excceded your search limit for the day",
    #     )
    search_in = SearchLogBase(ip_address=request.client.host, lasrra_id=lasrra_id)
    search_log_repo.create(db, obj_in=search_in)

    card_status_response = lasrra_api.track_card_status(lasrra_id)
    lga = None
    collection_center = None

    db_lga, db_collection_center = (
        db.query(LocalGovernment.name, CollectionCentre.name)
        .join(
            CollectionCentre, LocalGovernment.code == CollectionCentre.local_govt_code
        )
        .filter(
            LocalGovernment.code == card_status_response["lgaCode"],
            CollectionCentre.code == card_status_response["locationCode"],
        )
        .first()
    )

    if db_lga:
        lga = db_lga

    if db_collection_center:
        collection_center = db_collection_center

    return CardInfo(
        first_name=card_status_response.get("firstName", "N/A"),
        last_name=card_status_response.get("surname", "N/A"),
        lasrra_id=lasrra_id,
        replacement_id=card_status_response.get("replacementId", "N/A"),
        registration_status=card_status_response.get("registrationStatus", "N/A"),
        card_status=check_if_data(card_status_response.get("cardStatus", "N/A")),
        location=check_if_data(collection_center),
        lga=check_if_data(lga),
        isDelivered=check_card_is_delivered(
            card_status_response.get("cardStatus", "N/A")
        ),
    )


@router.post("/relocate_card")
def relocate_my_card(relocate_card: RelocateCard, db: Session = Depends(get_db)):
    source_local_government = (
        db.query(LocalGovernment)
        .filter(LocalGovernment.name == relocate_card.source_local_government)
        .first()
    )

    if not source_local_government:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Source LGA does not exist"
        )

    source_collection_center = (
        db.query(CollectionCentre)
        .filter(CollectionCentre.name == relocate_card.source_collection_centre)
        .first()
    )

    if not source_collection_center:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Source Collection Center does not exist",
        )

    destination_local_government = (
        db.query(LocalGovernment)
        .filter(LocalGovernment.name == relocate_card.destination_local_government)
        .first()
    )

    if not destination_local_government:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Destination LGA does not exist"
        )

    destination_collection_center = (
        db.query(CollectionCentre)
        .filter(CollectionCentre.name == relocate_card.destination_collection_centre)
        .first()
    )

    if not destination_collection_center:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Destination Collection Center does not exist",
        )

    relocate_card_data = {
        "lasrraId": relocate_card.lasrra_id,
        "fromLGACode": source_local_government.code,
        "fromLocationCode": source_collection_center.code,
        "DestinationLGACode": destination_local_government.code,
        "DestinationLocationCode": destination_collection_center.code,
    }

    relocate_result = lasrra_api.card_relocation(relocate_card_data)
    return relocate_result


@router.post("/deliver_card")
def deliver_my_card(deliver_card: DeliverCard, db: Session = Depends(get_db)):
    try:
        source_lga = (
            db.query(LocalGovernment)
            .filter(LocalGovernment.name == deliver_card.source_local_government)
            .first()
        )
        if not source_lga:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail="LGA does not exist"
            )

        source_location = (
            db.query(CollectionCentre)
            .filter(CollectionCentre.name == deliver_card.source_collection_centre)
            .first()
        )
        if not source_location:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Collection Center does not exist",
            )

        return "delivery_response"

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while delivering the card",
        )


@router.get("/get_masked_contact_details/{lasrra_id}")
def get_masked_contact_details(lasrra_id: str):
    try:
        masked_contacts = lasrra_api.fetch_masked_contact(lasrra_id)
        return masked_contacts
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching masked contact details",
        )


@router.post("/request_OTP")
def request_otp(otp_request: OTPRequest):
    try:
        lasrra_api.fetch_OTP(otp_request)
        return {"message": "OTP Sent Successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while requesting OTP",
        )


@router.post("/verify_OTP")
def verify_otp(verify_otp: VerifyOTP):
    try:
        lasrra_api.OTP_verification(verify_otp)
        return {"message": "OTP Verification Successful"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while verifying OTP",
        )
