from sqlalchemy import Column, String, Enum, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.core.common import AccountStatus

class EntAccount(Base):
    """
    企业账户（db model）
    """
    id = Column(Integer, primary_key=True, index=True)  # 用户账号，自动生成
    userAccount = Column(String)  # 用户在华通簿记系统中的账号

    enterpriseName = Column(String, nullable=False)  # 企业名称
    personName = Column(String, nullable=False)  # 法人姓名
    regAddress = Column(String, nullable=False)  # 企业注册地址
    businessLicenseCode = Column(String, index=True, unique=True, nullable=False)  # 营业执照号
    idIndate = Column(Date, nullable=False)  # 营业执照有效期
    personIdCode = Column(String, nullable=False)  # 法人身份证号
    personIdIndate = Column(Date, nullable=False)  # 法人身份证有效期
    nickName = Column(String, nullable=True)  # 用户昵称
    mobile = Column(String, nullable=False)  # 手机号码
    email = Column(String, nullable=True)  # 邮箱地址
    country = Column(String, nullable=False)  # 国籍、地区编码
    occupation = Column(String, nullable=False)  # 行业编码
    businessLicensePic = Column(String, nullable=False)  # 营业执照图片的Base64字符串
    personPicA = Column(String, nullable=False)  # 法人证件正面图片的Base64字符串
    personPicB = Column(String, nullable=False)  # 法人证件反面图片的Base64字符串
    licensePic = Column(String, nullable=True)  # 开户许可证图片的Base64字符串

    accountStatus = Column(Enum(AccountStatus), default=AccountStatus.pending)  # 账户状态

    cards = relationship("EntAccountCard", back_populates="owner")  # 绑定的银行卡


class EntAccountCard(Base):
    id = Column(Integer, primary_key=True, index=True)
    acctNo = Column(String, nullable=False)  # 绑定的银行账号
    acctName = Column(String, nullable=False)  # 绑定的银行账户名称
    opBankCode = Column(String, nullable=False)  # 开户行号
    opBankName = Column(String, nullable=False)  # 开户行名称

    owner = relationship("EntAccount", back_populates="cards")
    owner_id = Column(Integer, ForeignKey("entaccount.id"))
    # owner_userAccount = Column(String, ForeignKey("owner.userAccount"))
