from fastapi import APIRouter, Header

from app import schemas

router = APIRouter()

@router.post("/auth_ent_status/", summary="企业、个体工商户证件资料审核结果")
def auth_ent_status(auth_ent_status: schemas.AuthEntStatus, authorization: str = Header(...)):
    print(authorization)
    print(auth_ent_status)
    # TODO: 根据回调结果，修改数据库中相应账户状态、交易信息等
    return {"message": "I received, Thanks."}


@router.post("/settle_split_result/", summary="清算分账结果回调")
def settle_split_result(settle_split: schemas.SettleSplit, authorization: str = Header(...)):
    print(authorization)
    print(auth_ent_status)
    # TODO: 根据回调结果，修改数据库中相应账户状态、交易信息等
    return {"message": "I received, Thanks."}


@router.post("/withdraw_result/", summary="提现结果回调")
def withdraw_result(withdraw_result: schemas.WithdrawResult, authorization: str = Header(...)):
    print(authorization)
    print(auth_ent_status)
    # TODO: 根据回调结果，修改数据库中相应账户状态、交易信息等
    return {"message": "I received, Thanks."}
