import enum

from pydantic import BaseModel, Field

# class AuthStatus(str, enum.Enum):
#     pending = "0"  # 待审核
#     approved = "1"  # 审核通过
#     rejected = "2"  # 审核驳回


class AuthEntStatus(BaseModel):
    "企业/个体工商户证件资料审核结果回调报文"
    userAccount: str = Field(..., max_length=19, title="用户开户账户")
    authStatus: str = Field(..., title="审核状态")
    remark: str = Field(None, max_length=500, title="审核的具体信息")


class SettleSplit(BaseModel):
    "清算分账结果回调报文"
    industryCode: str = Field(..., title="平台方在华通的客户号")
    settleDate: str = Field(..., title="清算日期")  # 格式：yyyyMMdd
    batchNo: str = Field(..., title="批次号")
    content: str = Field(..., title="清算结果文件域")
    batchStatus: str = Field(..., title="批次状态")  # 0：整批失败  1：整批成功  2：部分成功


class WithdrawResult(BaseModel):
    "账户提现回调报文, TODO: 根据接口文档4.2.2的描述补充字段"
    pass