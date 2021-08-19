import os
import time  # 生成当前时间戳
import uuid  # 生成唯一流水号
import requests
from app.core.cfcasign import CFCASignature

def request(data, url):
    """
    上传数据给华通银行
    
    Arguments
    ---------
    data : dictionary
        需要上传的数据，字典，key和value都是字符串
    url : str
        上传url
    """

    # 第一步：把通用数据项：客户端流水号，加进去
    clientTradeId = uuid.uuid1().hex  # 生成唯一流水号
    data['clientTradeId'] = clientTradeId

    # 第二步，把数据字典按照key字符串排序，连接为数据字符串，如：key1=value1&key2=value2
    sorted_data = []
    for key, value in sorted(data.items()):
        sorted_data += [key+'='+value]
    sorted_data = '&'.join(sorted_data)

    # 第三步，在数据字符串后面追加时间戳字符串
    timestamp = int(round(time.time() * 1000))
    sorted_data = sorted_data + str(timestamp)
    
    # 第四步，调用cfca库对数据字符串加签
    pfx_file_name = 'JFJT.pfx'  # TODO: config
    cfca_signature = CFCASignature()
    res, signed_data = cfca_signature.get_sign(algorithm='rsa',
                            source_data=sorted_data,
                            pfx_file_name=pfx_file_name,
                            pfx_password='111111',  # TODO: config
                            hash_alg='sha-1')
    if res != 0:
        raise Exception('Sign error!')

    # 第五步，按照 'UTP01:' + 客户号 + ':' + 加签后数据 + ':' + 时间戳 格式生成authorization字符串
    industryCode = '005'  # 客户号，接入方在华通的唯一标识 TODO: config
    authorization = 'UTP01:' + industryCode + ':' + signed_data.decode() + ':' + str(timestamp)

    # 第六步，拼接url
    test_url = 'http://utptest.onebank.com.cn/v2/account/'  # TODO: config
    url = test_url + url

    # 第七步，调用requests库，上传数据
    headers = {'Authorization': authorization}
    r = requests.post(url, json=data, headers=headers)

    return r