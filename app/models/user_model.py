import jwt
from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy import Integer, Column, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship
from app.commonLib.models.base_class import Base
from app.core.settings.utilities import Utilities
from app.schemas.jwt_schema import JWTUser

from app.core.settings.config import Settings
# from app.core.services.security import AppSecurity




utils = Utilities()
settings = Settings()


JWT_EXPIRE_MINUTES=settings.JWT_EXPIRE_MINUTES
JWT_ALGORITHM= settings.JWT_ALGORITHM
SECRET_KEY =settings.SECRET_KEY
class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    @property
    def verify_password(self, password: str):
        return utils.verify_password(password, self.password)

    def hash_password(self, password:str):
        self.password= utils.get_password_hash(password)
    
    def generate_jwt(self, expires_delta: timedelta = None):
        if not self.is_active:
            raise Exception("user is not active")
        jwt_content = JWTUser(id=self.id, role=self.role).dict()
        if expires_delta is None:
            expires_delta = timedelta(minutes=JWT_EXPIRE_MINUTES)
        now = datetime.now()
        expires_at = now + expires_delta
        jwt_content["exp"] = expires_at.timestamp()
        jwt_content["iat"] = now.timestamp()
        encoded_token = jwt.encode(jwt_content, SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_token


