from sqlalchemy import Column, String, Enum, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.core.common import Sex, AccountStatus


class PersonalAccount(Base):
    id = Column(Integer, primary_key=True, index=True)  # 用户账号，自动生成
    userAccount = Column(String)  # 用户在华通簿记系统中的账号

    name = Column(String, index=True)  # 姓名
    idCode = Column(String, index=True, unique=True, nullable=False)  # 身份证号码
    nickName = Column(String) # 用户昵称
    mobile = Column(String, nullable=False)  # 手机号码
    email = Column(String, nullable=False) # 邮箱地址
    sex = Column(Enum(Sex), nullable=False)  # 性别
    country = Column(String, nullable=False)  # 国籍、地区编码
    profession = Column(String, nullable=False)  # 职业
    address = Column(String, nullable=False)  # 地址
    idIndate = Column(Date, nullable=False)  # 证件有效期
    personPicA = Column(String, nullable=False)  # 个人证件正面图片的Base64字符串"
    personPicB = Column(String, nullable=False)  # 个人证件反面图片的Base64字符串"

    accountStatus = Column(Enum(AccountStatus), default=AccountStatus.pending)  # 账户状态

    cards = relationship("PersonalAccountCard", back_populates="owner")  # 绑定的银行卡


class PersonalAccountCard(Base):
    id = Column(Integer, primary_key=True, index=True)
    acctNo = Column(String, nullable=False)  # 绑定的卡号
    mobile = Column(String, nullable=False)  # 预留的手机号

    owner = relationship("PersonalAccount", back_populates="cards")
    owner_id = Column(Integer, ForeignKey("personalaccount.id"))
    # owner_userAccount = Column(String, ForeignKey("owner.userAccount"))
