from typing import Any, List

from fastapi import APIRouter, Body, Query, Path, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.core.common import AccountStatus
from app.core.postman import request
from app.core.common import decode_base64_and_inflate

router = APIRouter()

# TODO: 不应该让用户输入华通的账号
@router.get("/status/{userAccount}", summary="账户状态")
def query_account_status(userAccount: str):
    data = {"userAccount": userAccount}
    url = "query_account_status"
    r = request(data, url)
    return r.json()


@router.get("/balance/platform/{industryCode}", summary="平台账户余额")
def query_balance(industryCode: str):
    data = {"industryCode": industryCode}
    url = "query_balance"
    r = request(data, url)
    return r.json()


@router.get("/balance/customer/{userAccount}", summary="个人、企业账户余额")
def query_balance(userAccount: str):
    data = {"userAccount": userAccount}
    url = "query_balance"
    r = request(data, url)
    return r.json()


@router.get("/list/platform/", summary="平台账户列表")
def plat_account_list():
    data = {}
    url = "plat_account_list"
    r = request(data, url)
    return r.json()


@router.get("/pay_flow/{batchNo}", summary="支付交易流水上送结果查询")
def query_industry_pay_flow_result(batchNo: str):
    data = {'batchNo': batchNo}
    url = "query_industry_pay_flow_result"
    r = request(data, url)
    return r.json()

@router.get("/query_settle_split/", summary="清算分账结果查询")
def query_settle_split(settleDate: str, batchNo: str):
    data = {
        'settleDate': settleDate,
        'batchNo': batchNo,
    }
    url = "query_settle_split"
    r = request(data, url)
    settle_split_result = r.json()["content"]
    print(decode_base64_and_inflate(settle_split_result.encode('utf-8')))
    return r.json()
