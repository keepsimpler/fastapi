from enum import Enum
from typing import Optional

import uvicorn
from fastapi import FastAPI, Body, Header  #, File, Form, UploadFile
from pydantic import BaseModel, Field

from app.api.api_v1.api import api_router
from app.core.config import settings

tags_metadata = [
    {
        "name": "Personal Accounts",
        "description": "个人账户开户、鉴权绑定、销户等业务",
    },
    {
        "name": "Enterprise Accounts",
        "description": "企业账户开户、鉴权绑定、销户等业务",
    },
    {
        "name": "Transactions",
        "description": "账户交易类业务，入金、分账、提现等",
    },
    {
        "name": "Queries",
        "description": "账户查询类业务，账户余额、账户状态、交易明细等",
    },
    {
        "name": "Huatong Callbacks",
        "description": "华通银行的回调"
    },
]


app = FastAPI(
    title = "EsPay",
    description = "Escroud以*RESTFul API*方式提供的支付接口",
    version = "0.1.0",
    openapi_tags = tags_metadata
)


# @app.get("/info")
# def info():
#     return {
#         "postgres_server": settings.POSTGRES_SERVER,
#         "postgres_user": settings.POSTGRES_USER,
#     }

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8090, reload=True)