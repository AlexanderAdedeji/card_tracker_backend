from app.models.user_model import User
from sqlalchemy.orm import Session
from app.commonLib.repositories import Base
from app.schemas.user_schema import UserCreate
from app.core.settings.utilities import Utilities


class UserRepositories(Base[User]):
    def get_by_email(self, db:Session, *, email):
        user = db.query(User).filter(User.email == email).first()
        return user

    def create(self, db:Session, *, obj_in: UserCreate):
        user_obj = User(
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            email=obj_in.email,
            hashed_password=Utilities.hash_password(obj_in.password),
        )
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return user_obj

    def reset_password(self, db: Session, *, db_obj: User, new_password: str):
        hashed_password = Utilities.hash_password(new_password)
        print(db_obj, new_password, hashed_password)
        return super().update(
            db, db_obj=db_obj, obj_in={"hashed_password": hashed_password}
        )
        

    def set_activation_status(self, db: Session, *, db_obj: User, status: bool):
        return super().update(db, db_obj=db_obj, obj_in={"is_active": status})

    def activate(self, db: Session, *, db_obj: User):
        return self.set_activation_status(db=db, db_obj=db_obj, status=True)

    def deactivate(self, db: Session, *, db_obj: User):
        return self.set_activation_status(db=db, db_obj=db_obj, status=False)
      
    def set_password_reset_check(self, db: Session, *, db_obj: User, status: bool):
        return super().update(db, db_obj=db_obj, obj_in={"password_reset": status})
        
    

user_repo = UserRepositories(User)
