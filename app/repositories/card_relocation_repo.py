from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from app.models.card_relocation_model import CardRelocation
from app.commonLib.repositories.repository_class import Base


class CardRelocationRepositories(Base[CardRelocation]):
    pass


card_relocation_repo = CardRelocationRepositories(CardRelocation)
