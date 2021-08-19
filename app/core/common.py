import enum
import zlib
import base64

class Sex(str, enum.Enum):
    male = "男"
    female = "女"

class AccountStatus(str, enum.Enum):
    """账户状态"""
    pending = '开户待审核'
    approved = '已开户，未绑卡'
    binded = '已开户，已绑卡'
    rejected = '审核驳回'


def deflate_and_base64_encode(string_: str) -> bytes:
    "对字符串先Deflate压缩，再Base64编码，返回bytes"
    bytes_ = string_.encode('utf-8')  # 转换为Byte String
    # 用zlib进行Deflate压缩
    compressed_bytes = zlib.compress(bytes_)
    # 去掉头部和尾部
    # compressed_bytes = compressed_bytes[2:-4]
    # Base64编码
    compressed_encoded_bytes = base64.b64encode(compressed_bytes)
    return compressed_encoded_bytes

def decode_base64_and_inflate(compressed_encoded_bytes: bytes) -> str:
    "对bytes先Base64解码，再Inflate解压缩，返回字符串"
    compressed_bytes = base64.b64decode(compressed_encoded_bytes)
    # 如果deflate时，去掉了头部和尾部，decompress需要加第二个参数-15
    bytes_ = zlib.decompress(compressed_bytes)
    string_ = bytes_.decode('utf-8')
    return string_

