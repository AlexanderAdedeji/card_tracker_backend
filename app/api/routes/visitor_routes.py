from fastapi import APIRouter, Request, Depends, status,HTTPException
from sqlalchemy.orm import Session
from app.api.requests.api_requests import (
    OTP_verification,
    card_relocation,
    fetch_card_name,
    fetch_masked_contact,
    requestOTP,
    track_card_status,
    validate_lasrraId,
)
from app.api.dependencies.db.db import get_db
from app.models.collection_centres import CollectionCentres
from app.models.local_government import LocalGovernments
from app.repositories.visit_repo import visit_repo
from app.schemas.card_schema import CardInfo
from app.schemas.visits_schema import OTPRequest, RelocateCard


router = APIRouter()


@router.get("/search")
async def visitor_get_status(
    request: Request, lasrra_id: str, db: Session = Depends(get_db)
):
    # is_limit_reached = visit_repo.check_ip_limit(db, ip=request.client.host)
    # if is_limit_reached:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="You have exceeded the limit, Check back",
    #     )
    print(type(request.client.host))
    visit_repo.create_visit(db, obj_in=request.client.host)
    validated_Id = validate_lasrraId(lasrra_id)
    card_name = fetch_card_name(lasrra_id)
    if validated_Id["code"] == "03":
        if validated_Id.get("replacementId"):
            lasrra_id = validated_Id.get("replacementId")
        else:
            return CardInfo(
                first_name=card_name["firstName"],
                last_name=card_name["surname"],
                lasrra_id=lasrra_id,
                status=f"{lasrra_id} Failed Validation",
                location="N/A",
                lga="N/A",
                isDelivered=False,
            )

    card_status = track_card_status(lasrra_id)
    if card_status == "NOT FOUND" or card_status == "FAILED":
        return CardInfo(
            first_name=card_name["firstName"],
            last_name=card_name["surname"],
            lasrra_id=lasrra_id,
            status=f"No card status for {lasrra_id}",
            location="N/A",
            lga="N/A",
            isDelivered=False,
        )

    db_lga = (
        db.query(LocalGovernments)
        .filter(LocalGovernments.code == card_status["lgaCode"])
        .first()
    )
    collection_center = (
        db.query(CollectionCentres)
        .filter(
            CollectionCentres.code == card_status["locationCode"],
            CollectionCentres.local_govt_code == card_status["lgaCode"],
        )
        .first()
    )

    return CardInfo(
        first_name=card_name["firstName"],
        last_name=card_name["surname"],
        lasrra_id=lasrra_id,
        status=card_status["status"],
        location=collection_center.name if collection_center else "N/A",
        lga=db_lga.name if db_lga else "N/A",
        is_delivered=card_status["status"].startswith("Delivered"),
    )


@router.post("/relocate_card")
def relocate_my_card(relocate_card: RelocateCard, db: Session = Depends(get_db)):
    OTP_verification(relocate_card)
    source_lga = (
        db.query(LocalGovernments)
        .filter(LocalGovernments.name == relocate_card.source_lg)
        .first()
    )
    source_location = (
        db.query(CollectionCentres)
        .filter(CollectionCentres.name == relocate_card.source_location)
        .first()
    )
    relocate_card_data = {
        "lasrraId": relocate_card.lasrra_id,
        "fromLGACode": source_lga.code,
        "fromLocationCode": source_location.code,
        "DestinationLGACode": relocate_card.destination_location,
        "DestinationLocationCode": relocate_card.destination_lg,
    }
    relocate_card = card_relocation(relocate_card_data)
    return relocate_card






@router.get("/get_masked_contact_details")
def get_masked_contact(lasrra_id: str):
    return fetch_masked_contact(lasrra_id)


@router.post("/requestOTP")
def requestForOTP(otp_request: OTPRequest):
    requestOTP(otp_request)
    return {"message": "OTP Sent Successfully"}
