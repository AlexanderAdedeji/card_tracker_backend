import json
from mimetypes import init
import requests
from fastapi import Request,  HTTPException, status
from app.schemas.visits_schema import RelocateCard, OTPRequest
from app.core.settings.config import AppSettings


settings = AppSettings()


def validate_lasrraId(lasrra_id: str):
    data = {'lasrraId': lasrra_id}
    is_card_valid = requests.post(
        f'{settings.LASRRA_IDENTITY_API}VerificationServices/verifystatus', json=data)
    if is_card_valid.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid ID Format")

    return is_card_valid.json()


def track_card_status(lasrra_id: str):
    card_status = requests.get(
        f'{settings.LASRRA_CARD_TRACKING_API}cardstatus/{lasrra_id}')
    if card_status.status_code == 404:
        return 'NOT_FOUND'
    if card_status.status_code != 200:
        return "FAILED"
        # print(card_status.json())
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        #                     detail=f'No card status for {lasrra_id}')

    return card_status.json()


def fetch_card_name(lasrra_id: str):
    card_name = requests.get(
        f'{settings.LASRRA_IDENTITY_API}RetrievalServices/getidnames/{lasrra_id}')
    print(card_name.json())
    if card_name.status_code != 200:
        raise HTTPException(status_code=card_name.status_code,
                            detail=card_name.json()["message"])
    if card_name.json()["message"] != "SUCCESSFUL":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=card_name.json()["message"])
    return card_name.json()


def card_relocation(relocate_card_data):
    relocate_card = requests.post(
        f"{settings.LASRRA_CARD_TRACKING_API}public/relocatemycard", json=relocate_card_data)
    if relocate_card.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=relocate_card.json())
    return relocate_card.json()


def OTP_verification(relocate_card: RelocateCard):
    verify_otp_data = {
        "lasrraId": relocate_card.lasrra_id,
        "code": relocate_card.otp
    }
    verify_otp = requests.post(
        f"{settings.LASRRA_IDENTITY_API}2fa/verifyotp", json=verify_otp_data)

    if verify_otp.status_code != 200:
        raise HTTPException(
            status_code=verify_otp.status_code, detail=verify_otp.json()["message"])
    if verify_otp.json()["message"] == "Match":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=(verify_otp.json()["message"]))
    return verify_otp


def fetch_masked_contact(lasrra_id: str):
    masked_contacts = requests.get(
        f"{settings.LASRRA_IDENTITY_API}2fa/getcontactoptions/{lasrra_id}")
    if masked_contacts.status_code != 200:
        raise HTTPException(status_code=masked_contacts.status_code,
                            detail=masked_contacts.json()['message'])

    return masked_contacts.json()


def requestOTP(otp_request: OTPRequest):
    data = {
        "channel": otp_request.channel,
        "lasrraId": otp_request.lasrra_id,
        "service": "LAGID"
    }
    response = requests.post(
        f"{settings.lasrra_identity_api}2fa/requestotp", json=data)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail=response.json()['message'])
    if response.json()['message'] != "SENT":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=response.json()['message'])

    return response.json()
