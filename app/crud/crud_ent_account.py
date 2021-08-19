from typing import Any, Dict, Optional, List

from fastapi.encoders import jsonable_encoder  # Convert pydantic model to json first, then it can be saved to db
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.ent_account import EntAccount, EntAccountCard
from app.schemas.ent_account import EntAccountCreate, EntAccountUpdate, EntAccountCardCreate, EntAccountCardUpdate


class CRUDEntAccount(CRUDBase[EntAccount, EntAccountCreate, EntAccountUpdate]):
    def get_by_businessLicenseCode(self, db:Session, *, businessLicenseCode: str) -> Optional[EntAccount]:
        return db.query(EntAccount).filter(EntAccount.businessLicenseCode == businessLicenseCode).first()


class CRUDEntAccountCard(CRUDBase[EntAccountCard, EntAccountCardCreate, EntAccountCardUpdate]):
    def create_with_owner(
        self, db:Session, *, obj_in:EntAccountCardCreate, owner_id: int, acctName: str,
    ) -> EntAccountCard:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id, acctName=acctName)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[EntAccountCard]:
        return(
            db.query(self.model).filter(EntAccountCard.owner_id == owner_id).offset(skip).limit(limit).all()
        )


ent_account = CRUDEntAccount(EntAccount)
ent_account_card = CRUDEntAccountCard(EntAccountCard)