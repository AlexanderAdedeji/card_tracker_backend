from typing import List
from sqlalchemy.orm import Session
from app.commonLib.repositories.repository_class import Base
from app.models.collection_centers_models import CollectionCentre
from app.models.local_goverment_models import LocalGovernment


class CollectionCenterRepositories(Base[CollectionCentre]):
    pass





class LocalGovernmentRepositories(Base[LocalGovernment]):
    pass






collection_center_repo = CollectionCenterRepositories(CollectionCentre)
local_govt_repo = LocalGovernmentRepositories(LocalGovernment)
