import enum
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from app.core.common import Sex, AccountStatus

# Shared properties
class PersonalAccountBase(BaseModel):
    name: str = Field(..., max_length=60, title="姓名", example="张三")  # 姓名
    idCode: str = Field(..., min_length=18, max_length=20, title="身份证号", example="110101199911120123")  # 身份证号码
    nickName: Optional[str] = Field(None, example="昵称")  # 用户昵称
    mobile: str = Field(..., min_length=11, max_length=15, title="手机号码", example="13939000001")  # 手机号码
    email: Optional[str] = Field(None, max_length=60, title="邮箱地址", example="info@example.com") # 邮箱地址
    sex: Sex  # 性别
    country: str = Field(..., title="国籍、地区编码", example="CHN")  # 国籍、地区编码
    profession: str = Field(..., title="职业", example="教师")  # 职业
    address: str = Field(..., title="地址", example="**地址")  # 地址
    idIndate: date = Field(..., title="证件有效期")  # 证件有效期
    personPicA: str = Field(..., title="个人证件正面图片的Base64字符串", example="Base64字符串")
    personPicB: str = Field(..., title="个人证件反面图片的Base64字符串", example="Base64字符串")
 
# Properties to receive via API on creation
class PersonalAccountCreate(PersonalAccountBase):
    accountStatus: Optional[AccountStatus] = Field(AccountStatus.pending, title="账户状态")

# TODO Properties to receive via API on update
class PersonalAccountUpdate(PersonalAccountBase):
    pass

# Properties to return via API
class PersonalAccount(PersonalAccountBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True


# Shared properties
class PersonalAccountCardBase(BaseModel):
    acctNo: str = Field(..., title="绑定的银行卡号", example="6200861111111110001")
    mobile: str = Field(..., title="在银行预留的手机号", example="13939000001")

# Properties to receive via API on creation
class PersonalAccountCardCreate(PersonalAccountCardBase):
    pass

# TODO Properties to receive via API on update
class PersonalAccountCardUpdate(PersonalAccountCardBase):
    pass

# Properties to return via API
class PersonalAccountCard(PersonalAccountCardBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
