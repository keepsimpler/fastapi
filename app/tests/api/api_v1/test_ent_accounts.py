import os
import base64

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings


def test_create_ent_account(
    client: TestClient, db: Session
) -> None:
    current_path = os.path.dirname(os.path.abspath(__file__))  # 获得当前目录
    file_path = os.path.join(current_path, '身份证正面2.jpg')
    with open(file_path, 'rb') as f:
        personPicA = base64.b64encode(f.read()).decode()
    file_path = os.path.join(current_path, '身份证反面2.jpg')
    with open(file_path, 'rb') as f:
        personPicB = base64.b64encode(f.read()).decode()

    data = {
        # 'userNo': 'undefined',  # 接入方用户号
        'enterpriseName': '双敏电子传媒有限公司',  # 企业名称
        'personName': '叶斌',  # 法人姓名
        'regAddress': '辽宁省瑜县房山北京街L座 260558',  # 企业注册地址
        'businessLicenseCode': '513436199108292183',  # 营业执照号
        'idIndate': '2025-12-01',  # 营业执照有效期
        # 'personIdType': '101',  # 法人证件类型
        'personIdIndate': '2030-12-01',  # 法人证件有效期
        'personIdCode': '513436199108292183',  # 法人证件号码  
        'nickName': '昵称',  # 用户昵称
        'mobile': '13939111111',  # 手机号码
        'email': 'admin@example.com',  # 邮箱地址
        # 'nature': '2',  # 账户性质 2-普通账户 7-佣金账户
        'country': 'CHN',  # 国籍、地区编码
        'occupation': 'I',  # 行业
        'businessLicensePic': personPicA,  # 营业执照图片
        'personPicA': personPicA,  # 个人证件正面图片 Base64字符串
        'personPicB': personPicB,  # 个人证件反面图片 Base64字符串
        'licensePic': personPicB,  # 开户许可证
    }
    url = f"{settings.API_V1_STR}/accounts/enterprise/"

    r = client.post(url, json=data)


