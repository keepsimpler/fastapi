from typing import Any, Dict, Optional, Union, List

from fastapi.encoders import jsonable_encoder  # Convert pydantic model to json first, then it can be saved to db
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.personal_account import PersonalAccount, PersonalAccountCard
from app.schemas.personal_account import PersonalAccountCreate, PersonalAccountUpdate, PersonalAccountCardCreate, PersonalAccountCardUpdate


class CRUDPersonalAccount(CRUDBase[PersonalAccount, PersonalAccountCreate, PersonalAccountUpdate]):
    def get_by_idCode(self, db:Session, *, idCode: str) -> Optional[PersonalAccount]:
        return db.query(PersonalAccount).filter(PersonalAccount.idCode == idCode).first()


class CRUDPersonalAccountCard(CRUDBase[PersonalAccountCard, PersonalAccountCardCreate, PersonalAccountCardUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: PersonalAccountCardCreate, owner_id: int
    ) -> PersonalAccountCard:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100 
    ) -> List[PersonalAccountCard]:
        return(
            db.query(self.model).filter(PersonalAccountCard.owner_id == owner_id).offset(skip).limit(limit).all()
        )

personal_account = CRUDPersonalAccount(PersonalAccount)

personal_account_card = CRUDPersonalAccountCard(PersonalAccountCard)