from pydantic import BaseModel
from typing import Optional


class Card(BaseModel):
    lasrra_id: str

class CardInfo(Card):
    first_name: str
    last_name: str
    registration_status:str
    replacement_id:Optional[str]
    card_status: str
    collection_center: str
    local_government:str
    isDelivered:bool

class OTPRequest(Card):
    channel: str


class VerifyOTP(Card):
    code: str


class RelocateCard(Card):
    destination_local_government: str
    destination_collection_centre: str
    source_local_government: str
    source_collection_centre: str


class DeliverCard(Card):
    source_local_government: str
    source_collection_centre: str
    deliver_to: str
    transaction_ref: str
