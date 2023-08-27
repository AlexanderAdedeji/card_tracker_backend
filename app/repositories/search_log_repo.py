from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from app.models.search_log_models import SearchLog
from app.commonLib.repositories.repository_class import Base


class SearchLogRepositories(Base[SearchLog]):
    def check_ip_search_limit(self, db: Session, *, ip: str):
        today = datetime.now().strftime("%Y-%m-%d")
        is_limit_exceeded = (
            db.query(SearchLog)
            .filter(
                SearchLog.ip_address == ip,
                func.to_char(SearchLog.created_at, "YYYY-MM-DD") == today,
            )
            .count()
        )
        return is_limit_exceeded >= 3


search_log_repo = SearchLogRepositories(SearchLog)
