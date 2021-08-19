from typing import Optional
from datetime import date

from pydantic import BaseModel, Field

from app.core.common import AccountStatus

# Shared properties
class EntAccountBase(BaseModel):
    enterpriseName: str = Field(..., title="企业名称", example="**公司")
    personName: str = Field(..., title="法人姓名")
    regAddress: str = Field(..., title="企业注册地址")
    businessLicenseCode: str = Field(..., title="营业执照号")
    idIndate: date = Field(..., title="营业执照有效期")
    personIdCode: str = Field(..., title="法人身份证号")
    personIdIndate: date = Field(..., title="法人身份证有效期")
    nickName: Optional[str] = Field(..., title="用户昵称")
    mobile: str = Field(..., title="手机号码")
    email: Optional[str] = Field(..., title="邮箱地址")
    country: str = Field(..., title="国籍、地区编码", example="CHN")
    occupation: str = Field(..., title="行业编码", example="I")
    businessLicensePic: str = Field(..., title="营业执照图片的Base64字符串", example="Base64字符串")
    personPicA: str = Field(..., title="法人证件正面图片的Base64字符串", example="Base64字符串")
    personPicB: str = Field(..., title="法人证件反面图片的Base64字符串", example="Base64字符串")
    licensePic: Optional[str] = Field(..., title="开户许可证图片的Base64字符串", example="Base64字符串")

# Properties to receive via API on creation
class EntAccountCreate(EntAccountBase):
    accountStatus: Optional[AccountStatus] = Field(AccountStatus.pending, title="账户状态")
    userAccount: Optional[str] = Field(None, title="华通簿记系统中的账号")

# TODO Properties to receive via API on update
class EntAccountUpdate(EntAccountBase):
    pass

# Properties to return via API
class EntAccount(EntAccountBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True




# Shared properties
class EntAccountCardBase(BaseModel):
    acctNo: str = Field(..., title="绑定的银行账号", example="6200861111111111001")
    # acctName: str = Field(..., title="绑定的银行账户名称", example="**公司")
    opBankCode: str = Field(..., title="开户行号", example="102100099996")
    opBankName: str = Field(..., title="开户行名称", example="工行**支行")
    # clBankCode: Optional[str] = Field(..., title="清算行号")

# Properties to receive via API on creation
class EntAccountCardCreate(EntAccountCardBase):
    pass

# TODO Properties to receive via API on update
class EntAccountCardUpdate(EntAccountCardBase):
    pass

# Properties to return via API
class EntAccountCard(EntAccountCardBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
