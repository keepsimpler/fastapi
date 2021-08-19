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


@router.get('/', response_model=List[schemas.PersonalAccount], summary="个人账户列表")
def read_personal_accounts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve personal accounts
    """
    personal_accounts = crud.personal_account.get_multi(db, skip=skip, limit=limit)
    return personal_accounts


@router.post('/', response_model=schemas.PersonalAccount, summary="个人开户")  # 
def create_personal_account(
    *,
    db: Session = Depends(deps.get_db),
    personal_account_in: schemas.PersonalAccountCreate,
) -> Any:
    """
    Create new personal account.
    """
    # 1. 按身份证号查找该用户是否已经存在，如果该用户已经存在，返回400错误
    personal_account = crud.personal_account.get_by_idCode(db, idCode=personal_account_in.idCode)
    if personal_account:  # 
        raise HTTPException(
            status_code=400,
            detail="The personal account with this idCode (身份证号) already exists in the system.",
        )

    # 2. 组织向华通发送的data和url，并发送
    data = {
        'userNo': 'undefined',  # 接入方用户号
        'name': personal_account_in.name,  # 用户真实姓名 测试2
        'idType': '101',  # 证件类型
        'idCode': personal_account_in.idCode,  # 证件号码  110101198001010037
        'nickName': personal_account_in.nickName,  # 用户昵称
        'mobile': personal_account_in.mobile,  # 手机号码
        'email': personal_account_in.email,  # 邮箱地址
        'sex': 'M' if personal_account_in.sex == '男' else 'F',  # 性别：M男 F女
        'country': personal_account_in.country,  # 国籍、地区编码
        'prosession': personal_account_in.profession,  # 职业, 应该是：profession
        'address': personal_account_in.address,  # 住所/工作地点
        'idIndate': str(personal_account_in.idIndate),  # 证件有效期
        'personPicA': personal_account_in.personPicA,  # 个人证件正面图片 Base64字符串
        'personPicB': personal_account_in.personPicB,  # 个人证件反面图片 Base64字符串
        'nature': '3'  # 账户性质 3-个人账户
    }
    url = 'open_account'

    r = request(data, url)

    # 3. 如果华通审核通过，则insert到数据库表中;否则，把华通返回的错误转送给客户端
    # TODO 需要把华通返回的账号userAccount加入到记录中
    if 200 <= r.status_code < 300:
        personal_account_in.accountStatus = AccountStatus.approved
        personal_account = crud.personal_account.create(db, obj_in=personal_account_in)
    else:
        raise HTTPException(
            status_code=r.status_code,
            detail=r.json()['message'],
        )

    return personal_account


@router.get("/{owner_id}/cards/", response_model=List[schemas.PersonalAccountCard], summary="个人账户绑定的银行卡列表")
def read_personal_account_cards(
    db: Session = Depends(deps.get_db),
    owner_id: int = Path(..., title="个人账户id"),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve cards binded to a personal account.
    """
    cards = crud.personal_account_card.get_multi_by_owner(db=db, owner_id=owner_id, skip=skip, limit=limit)
    return cards

@router.post("/{owner_id}/cards/", response_model=schemas.PersonalAccountCard, summary="个人账户银行卡绑定")  # 
def create_personal_account_card(
    *,
    db: Session = Depends(deps.get_db),
    owner_id: int = Path(..., title="个人账户id"),
    personal_account_card_in: schemas.PersonalAccountCardCreate,
) -> Any:
    """
    Bind new card for a personal account.
    """
    # 1. 根据id，获得个人账户在华通的账号
    personal_account = crud.personal_account.get(db=db, id=owner_id)

    # 2. 组织向华通发送的data和url，并发送
    data = {
        'userAccount': personal_account.userAccount,  # 用户开户账户
        'verifyType': '4',  # 验证类型 4：四要素验证
        'acctNo': personal_account_card_in.acctNo,  # 绑定的银行卡号
        'mobile': personal_account_card_in.mobile,  # 预留手机号码
    }
    url = 'bind'
    r = request(data, url)

    # 3. 如果华通审核通过，则insert到数据库表中;否则，把华通返回的错误转送给客户端
    if r.json()['status'] == '200':
        personal_account_card = crud.personal_account_card.create_with_owner(db=db, obj_in=personal_account_card_in, owner_id=owner_id)
        return personal_account_card
    else:
        raise HTTPException(
            status_code = int(r.json()['status']),
            detail = r.json()['message']
        )

