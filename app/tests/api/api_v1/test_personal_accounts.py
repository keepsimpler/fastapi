import os
import base64

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# from app import crud
from app.core.config import settings
# from app.schemas.account import PersonalAccountCreate

def test_create_personal_account_card(
    client: TestClient, db: Session
) -> None:
    data = {
        # TODO
    }


def test_create_personal_account(
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
        # 'userNo': 'person1',  # 接入方用户号
        'name': '冯文峰',  # 用户真实姓名 测试2
        # 'idType': '101',  # 证件类型
        'idCode': '110101198001010037',  # 证件号码  110101198001010037
        'nickName': 'keepsimpler',  # 用户昵称
        'mobile': '13939222222',  # 手机号码
        'email': 'fengwenfeng@gmail.com',  # 邮箱地址
        'sex': '男',  # 性别：M男 F女
        'country': 'CHN',  # 国籍、地区编码
        'profession': '20000',  # 职业, 应该是：profession
        'address': '********',  # 住所/工作地点
        'idIndate': '2025-05-29',  # 证件有效期
        'personPicA': personPicA,  # 个人证件正面图片 Base64字符串
        'personPicB': personPicB,  # 个人证件反面图片 Base64字符串
        # 'nature': '3'  # 账户性质 3-个人账户
    }

    url = f"{settings.API_V1_STR}/accounts/personal/"
   
    r = client.post(url, json=data)
    print(r.json())
    assert 200 <= r.status_code < 300 or r.status_code == 400
    if r.status_code == 400:
        print("The personal account with this idCode (身份证号) already exists in the system.")
    else:
        created_personal_account = r.json()
        print(created_personal_account)
