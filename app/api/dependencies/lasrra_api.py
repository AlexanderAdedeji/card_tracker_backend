import requests
from fastapi import HTTPException
from app.schemas.card_management_schema import VerifyOTP, OTPRequest
from app.core.settings.config import Settings

class LasrraAPI:
    def __init__(self):
        self.settings = Settings()

    def _api_request(self, api_type, endpoint, method="GET", json_data=None):
        base_url = (
            self.settings.LASRRA_CARD_TRACKING_API
            if api_type == "tracking"
            else self.settings.LASRRA_IDENTITY_API
        )
        response = requests.request(
            method,
            f"{base_url}{endpoint}",
            json=json_data,
        )
        print(f"{base_url}{endpoint}")
        response_json = response.json()

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail=response_json["message"]
            )

        return response_json

    def _lasrra_card_tracking_api_request(self, endpoint, method="GET", json_data=None):
        return self._api_request("tracking", endpoint, method, json_data)

    def _lasrra_identity_api_request(self, endpoint, method="GET", json_data=None):
        return self._api_request("identity", endpoint, method, json_data)

    def validate_lasrra_id(self, lasrra_id: str):
        data = {"lasrraId": lasrra_id}
        return self._lasrra_identity_api_request("VerificationServices/verifystatus", method="POST", json_data=data)

    def track_card_status(self, lasrra_id: str):
        return self._lasrra_card_tracking_api_request(f"cardstatus/{lasrra_id}")

    def fetch_card_name(self, lasrra_id: str):
        return self._lasrra_identity_api_request(f"RetrievalServices/getidnames/{lasrra_id}")

    def card_relocation(self, relocate_card_data):
        return self._lasrra_card_tracking_api_request("relocatemycard", method="POST", json_data=relocate_card_data)

    def OTP_verification(self, verify_otp: VerifyOTP):
        verify_otp_data = {"lasrraId": verify_otp.lasrra_id, "code": verify_otp.code}
        return self._lasrra_identity_api_request("2fa/verifyotp", method="POST", json_data=verify_otp_data)

    def fetch_masked_contact(self, lasrra_id: str):
        return self._lasrra_identity_api_request(f"2fa/getcontactoptions/{lasrra_id}")

    def fetch_OTP(self, otp_request: OTPRequest):
        data = {
            "channel": otp_request.channel,
            "lasrraId": otp_request.lasrra_id,
            "service": "LAGID",
        }
        return self._lasrra_identity_api_request("2fa/requestotp", method="POST", json_data=data)
