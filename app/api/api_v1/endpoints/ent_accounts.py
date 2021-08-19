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


@router.get('/', response_model=List[schemas.EntAccount], summary="企业账户列表")
def read_ent_accounts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrive enterprise accounts
    """
    ent_accounts = crud.ent_account.get_multi(db, skip=skip, limit=limit)
    return ent_accounts


@router.post('/', response_model=schemas.EntAccount, summary="企业开户")
def create_ent_account(
    *,
    db: Session = Depends(deps.get_db),
    ent_account_in: schemas.EntAccountCreate,
) -> Any:
    """
    Create new enterprise account.
    """
    # 1. 按营业执照号查找该用户是否已经存在，如果存在，返回400错误
    ent_account = crud.ent_account.get_by_businessLicenseCode(db, businessLicenseCode=ent_account_in.businessLicenseCode)
    if ent_account:
        raise HTTPException(
            status_code=400,
            detail="The enterprise account with this businessLicenseCode (营业执照号) already exists in the system."
        )

    # 2. 组织向华通发送的data和url，并发送
    # data = {
    #     'userNo': 'undefined',  # 接入方用户号
    #     'enterpriseName': ent_account_in.enterpriseName,  # 企业名称
    #     'personName': ent_account_in.personName,  # 法人姓名
    #     'regAddress': ent_account_in.regAddress,  # 企业注册地址
    #     'businessLicenseCode': ent_account_in.businessLicenseCode,  # 营业执照号
    #     'idIndate': ent_account_in.idIndate,  # 营业执照有效期
    #     'personIdType': '101',  # 法人证件类型
    #     'personIdIndate': ent_account_in.personIdIndate,  # 法人证件有效期
    #     'personIdCode': ent_account_in.personIdCode,  # 法人证件号码  
    #     'nickName': ent_account_in.nickName,  # 用户昵称
    #     'mobile': ent_account_in.mobile,  # 手机号码
    #     'email': ent_account_in.email,  # 邮箱地址
    #     'nature': '2',  # 账户性质 2-普通账户 7-佣金账户
    #     'country': ent_account_in.country,  # 国籍、地区编码
    #     'occupation': ent_account_in.occupation,  # 行业
    #     'businessLicensePic': ent_account_in.businessLicensePic,  # 营业执照图片
    #     'personPicA': ent_account_in.personPicA,  # 个人证件正面图片 Base64字符串
    #     'personPicB': ent_account_in.personPicB,  # 个人证件反面图片 Base64字符串
    #     'licensePic': ent_account_in.licensePic,  # 开户许可证
    #     'callbackUrl': 'http://pay.escroud.com:8090/callbacks/huatong/auth_ent_status/',  # 企业证件资料审核回调地址  TODO: 需要修改到云主机地址
    # }
    # url = 'new_open_account_ent'

    # r = request(data, url)

    # 3. TODO 根据华通返回的结果，写入数据库表，或转发错误信息给客户端
    ent_account_in.accountStatus = AccountStatus.approved
    ent_account_in.userAccount = '9100001101000007103'  # FIXME TODO
    ent_account = crud.ent_account.create(db, obj_in=ent_account_in)

    return ent_account


@router.get("/{owner_id}/cards/", response_model=List[schemas.EntAccountCard], summary="企业账户绑定的银行账号列表")
def read_ent_account_cards(
    db: Session = Depends(deps.get_db),
    owner_id: int = Path(..., title="企业账户id"),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrive cards binded to a enterprise account.
    """
    cards = crud.ent_account_card.get_multi_by_owner(db=db, owner_id=owner_id, skip=skip, limit=limit)
    return cards

@router.post("/{owner_id}/cards/", summary="企业账户绑定银行账户") # , response_model=schemas.EntAccountCard
def create_ent_account_card(
    *,
    db: Session = Depends(deps.get_db),
    owner_id: int = Path(..., title="企业账户id"),
    ent_account_card_in: schemas.EntAccountCardCreate,
) -> Any:
    """
    Bind new card for an enterprise account.
    """
    # 1. 根据id，获得企业账户在华通簿记系统中的账号
    ent_account = crud.ent_account.get(db=db, id=owner_id)

    # 2. 如果该账户状态不是approved，则返回400错误
    if ent_account.accountStatus != AccountStatus.approved:
        raise HTTPException(
            status_code = "400",
            detail = "账户状态错误。Only approved accounts can bind to bank account."
        )

    # 3. 组织向华通发送的data和url，并发送
    data = {
        'userAccount': ent_account.userAccount,  # 华通簿记系统中的企业账号
        'acctNo': ent_account_card_in.acctNo,  # 绑定的银行账号
        'acctName': ent_account.enterpriseName,  # 账户名称，必须与华通簿记系统中的名称一致！
        'opBankCode': ent_account_card_in.opBankCode,  # 开户行号
        'opBankName': ent_account_card_in.opBankName,
    }
    url = 'new_auth_bind_ent'

    r = request(data, url)

    # 3. 如果华通审核通过，则insert到数据库表中;否则，把华通返回的错误转送给客户端
    if r.json()['status'] == '200':
        ent_account_card = crud.ent_account_card.create_with_owner(db=db, obj_in=ent_account_card_in, owner_id=owner_id, acctName=ent_account.enterpriseName)
        return ent_account_card
    else:
        raise HTTPException(
            status_code = int(r.json()['status']),
            detail = r.json()['message']
        )
