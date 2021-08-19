from typing import Any, List

from fastapi import APIRouter, Body, Query, Path, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.core.common import AccountStatus
from app.core.postman import request

router = APIRouter()

@router.get('/split', summary="分账")
def withdraw():
    pass

@router.get('/withdraw', summary="提现")
def withdraw():
    pass
