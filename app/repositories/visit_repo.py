from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from app.models.visits_models import Visits
from app.schemas.visits_schema import CreateVisits
from app.commonLib.repositories import Base



class VisitsRepositories(Base[Visits]):
    def get_by_ip(self, db:Session, ip: str):
        return db.query(Visits).filter(Visits.visit_ip_address == ip).first()

    def create_visit(self, db:Session, obj_in: str):
        db_obj = Visits(visit_ip_address=obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def check_ip_limit(self, db:Session, ip: CreateVisits):
        is_limit_exceeded = (
            db.query(Visits)
            .filter(
                Visits.visit_ip_address == ip
                and func.to_char(Visits.created_at("%Y-%m-%d"))
                == datetime.now().strftime("%Y-%m-%d")
            )
            .count()
        )
        if is_limit_exceeded < 3:
            return False
        else:
            return True


visit_repo = VisitsRepositories(Visits)
