import uuid
from app.commonLib.repositories.repository_class import Base
from app.core.settings.utilities import Utilities
from app.models.user_model import User
from app.schemas.user_schema import UserCreateForm




utils = Utilities()





class UserRepositories(Base[User]):
    def get_by_email(self, db,*,email:str ):
        return self.get_by_field(db, field_name="email", field_value=email)
    def create(self, db, *, obj_in:UserCreateForm):
        db_obj = User(
            id=str(uuid.uuid4()),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            role=obj_in.role.upper(),
            is_active = False,
            email =obj_in.email,
         
        )
        db_obj.hash_password(obj_in.password)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    pass





user_repo =UserRepositories(User)