#%%
from app.core.postman import request

from app.core.common import decode_base64_and_inflate, deflate_and_base64_encode
# %% 支付流水上传
pay_flow = """H|pay_flow|20210513|2
20210513|123029|9001000112347|9001|1500|0|凡客旗舰店|张三|T恤衫|备注说明|139888866666|Z2000133000019|ch0001|userId1|13877778888|0|无
20210513|123128|9001000112348|9001|300|3|凡客旗舰店|李四|球鞋|备注说明|139888866667|Z2000133000019|ch0002|userId2|13877778889|0|无
"""

#%%
compressed_encoded_pay_flow = deflate_and_base64_encode(pay_flow)
print(compressed_encoded_pay_flow)
decode_base64_and_inflate(compressed_encoded_pay_flow) == pay_flow
#%%
data = {
    'reqDate': '20210513',  # 请求日期，格式：yyyyMMdd
    'reqTime': '130101',  # 请求时间，格式：HHmmss
    'batchNo': '00000002',  # 批次号，全局唯一
    'content': compressed_encoded_pay_flow.decode(),  # 支付流水文件域
}
# %%
url = 'upload_industry_pay_flow'
# %%
r = request(data, url)
# %%
r.json()


#%%  清算分账上传
settle = """H|settle|20210514|2
20210514|90010005|9100001101000007103|1500|1|0|T+0记账清算|9001000112347|扩展2|扩展3
20210514|90010006|9100001101000007103|300|1|0|T+0记账清算|9001000112348|扩展2|扩展3
"""
# %%
compressed_encoded_settle = deflate_and_base64_encode(settle)
print(compressed_encoded_settle)
decode_base64_and_inflate(compressed_encoded_settle) == settle

# %%
callbackUrl = 'http://pay.escroud.com:8090/api/v1/callbacks/huatong/settle_split_result/'
data = {
    'reqDate': '20210514',  # 请求日期，格式：yyyyMMdd
    'reqTime': '120101',  # 请求时间，格式：HHmmss
    'settleDate': '20210514', # 清算日期
    'batchNo': '00000003',  # 批次号，全局唯一
    'callbackUrl': callbackUrl,  # 回调地址
    'content': compressed_encoded_settle.decode(),  # 清算分账文件域
}
# %%
url = 'upload_settle_split'
# %%
r = request(data, url)
# %%
r.json()

# %% 账户提现
callbackUrl = 'http://pay.escroud.com:8090/api/v1/callbacks/huatong/withdraw_result/'

data = {
    'userAccount': '9100001101000007103',  # 用户账户
    'reqDate': '20210521',  # 请求日期
    'reqTime': '161301',  # 请求时间
    'payAmt': '1000',  # 提现金额，单位分
    'callbackUrl': callbackUrl,  # 回调地址
    'remark': '提现',  # 备注说明
    'acctNo': '6200861111111111001',  # 绑定的银行账号
}

url = 'withdraw'
# %%
r = request(data, url)
# %%
r.json()


# %% 交易结果（账户提现结果）查询

data = {
    'reqDate': '20210521',  # 请求日期，原交易请求日期
    'origClientTradeId': '2de99360ba1111eba88f52540054d9d4',  # 原客户端流水号
    'origServerTradeId': '20210521HM030449395662517266591746',  # 原服务端流水号
}

url = 'query_withdraw'
# %%
r = request(data, url)
# %%
r.json()

# 返回的查询结果
query_withdraw_result = 
{'clientTradeId': '07f6cec4ba1211eba88f52540054d9d4',
 'serverTradeId': '20210521HM030449395664051899510786',
 'status': '200',
 'message': '查询成功',
 'timestamp': '2021-05-21T16:53:34.853',
 'origClientTradeId': '2de99360ba1111eba88f52540054d9d4',
 'origServerTradeId': '20210521HM030449395662517266591746',
 'transStatus': 'TRADE_SUCCESS',
 'statusDesc': '交易成功',
 'reconcileDate': '20210524',
 'feeType': '2',
 'feeModel': '2',
 'feeAmount': '100'}


# %%
