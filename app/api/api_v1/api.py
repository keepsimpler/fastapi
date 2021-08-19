from fastapi import APIRouter

from app.api.api_v1.endpoints import personal_accounts
from app.api.api_v1.endpoints import ent_accounts
from app.api.api_v1.endpoints import queries
from app.api.api_v1.endpoints import huatong_callbacks
from app.api.api_v1.endpoints import transcations


api_router = APIRouter()
api_router.include_router(personal_accounts.router, prefix="/accounts/personal", tags=["Personal Accounts"])
api_router.include_router(ent_accounts.router, prefix="/accounts/enterprise", tags=["Enterprise Accounts"])
api_router.include_router(queries.router, prefix="/accounts/queries", tags=["Queries"])
api_router.include_router(huatong_callbacks.router, prefix="/callbacks/huatong", tags=["Huatong Callbacks"])
api_router.include_router(transcations.router, prefix="/transactions", tags=["Transactions"])