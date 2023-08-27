import requests
from fastapi import HTTPException, status
from app.schemas.card_management_schema import VerifyOTP, OTPRequest
from app.core.settings.config import Settings


class LasrraAPI:
    def __init__(self):
        self.settings = Settings()

    def _api_request(self, endpoint, method="GET", json_data=None):
        response = requests.request(
            method,
            f"{self.settings.LASRRA_IDENTITY_API}{endpoint}",
            json=json_data,
        )
        print(  f"{self.settings.LASRRA_IDENTITY_API}{endpoint}")
        response_json = response.json()

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail=response_json["message"]
            )

        return response_json
        return response
    def validate_lasrra_id(self, lasrra_id: str):
        data = {"lasrraId": lasrra_id}
        return self._api_request(
            "VerificationServices/verifystatus", method="POST", json_data=data
        )

    def track_card_status(self, lasrra_id: str):
        return self._api_request(f"cardstatus/{lasrra_id}")

    def fetch_card_name(self, lasrra_id: str):
        return self._api_request(f"RetrievalServices/getidnames/{lasrra_id}")

    def card_relocation(self, relocate_card_data):
        return self._api_request("relocatemycard", method="POST", json_data=relocate_card_data)

    def OTP_verification(self, verify_otp: VerifyOTP):
        verify_otp_data = {"lasrraId": verify_otp.lasrra_id, "code": verify_otp.code}
        return self._api_request("2fa/verifyotp", method="POST", json_data=verify_otp_data)

    def fetch_masked_contact(self, lasrra_id: str):
        return self._api_request(f"2fa/getcontactoptions/{lasrra_id}")

    def fetch_OTP(self, otp_request: OTPRequest):
        data = {
            "channel": otp_request.channel,
            "lasrraId": otp_request.lasrra_id,
            "service": "LAGID",
        }
        return self._api_request("2fa/requestotp", method="POST", json_data=data)
