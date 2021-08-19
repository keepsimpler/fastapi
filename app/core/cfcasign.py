import os
import base64
from ctypes import cdll, pointer, c_char_p

class CFCASignature:
    def __init__(self):
        self.current_path = os.path.dirname(os.path.abspath(__file__))  # 获得当前目录
        so_file_path = os.path.join(self.current_path, 'lib', 'libSADK_Standard.so.3.4.1.2')
        self.so = cdll.LoadLibrary(so_file_path)
        res = self.so.Initialize()
        if res != 0:
            raise Exception('Init so file error')
        self.sign_data = c_char_p(b'')
        self.cert = c_char_p(b'')

    def get_sign(self, algorithm, source_data, pfx_file_name, pfx_password, hash_alg):
        """
        获取签名

        Arguments
        ---------
        algorithm : str
            签名算法
        source_data : str
            待签名原文
        pfx_file_name : str
            pfx文件名
        pfx_password : str
            pfx文件密码
        hash_alg : str
            哈希算法

        Returns
        -------
        int
            状态码，0表示正确，非0表示错误
        str
            签名后数据

        """
        # 获得pfx文件路径
        pfx_file_path = os.path.join(self.current_path, 'lib', pfx_file_name)

        algorithm = self._str2bytes(algorithm, 'ascii')
        source_data = self._str2bytes(source_data, "utf-8")
        pfx_file_path = self._str2bytes(pfx_file_path, 'ascii')
        pfx_password = self._str2bytes(pfx_password, 'ascii')
        hash_alg = self._str2bytes(hash_alg, 'ascii')

        source_size = len(source_data)
        base64_pkcs7_detached_signature = pointer(self.sign_data)  # 保存返回的签名后数据

        res = self.so.SignData_PKCS7Detached(algorithm,
                                       source_data,
                                       source_size,
                                       pfx_file_path,
                                       pfx_password,
                                       hash_alg,
                                       base64_pkcs7_detached_signature)
        return res, self.sign_data.value

    def check_sign(self, base64_signature, algorithm):
        """
        验证签名

        Arguments
        ---------
        base64_signature : str
            base64 格式的签名数据
        algorithm : str
            算法

        Returns
        -------
        res
        :
        int
            状态码，0表示正确，非0表示错误
        str
            签名前数据

        FIXME: Detached和Attached验签时的传入参数不同，需要仔细研究！！
        """
        sign_str = base64.b64decode(base64_signature)

        byte_size = c_int(0)
        p_byte_size = pointer(byte_size)

        p_cert = pointer(self.cert)

        source_data = c_char_p(b'')
        p_source_data = pointer(source_data)

        res = self.so.VerifyDataSignature_PKCS7Detached(algorithm, sign_str, p_cert, p_source_data, p_byte_size)
        return res, source_data.value[0:byte_size.value]

    @staticmethod
    def _str2bytes(string, encoding):
        '''Takes in string, Convert to and return bytes using encoding method'''
        return string.encode(encoding=encoding)

    def __del__(self):
        # TODO: 调用FreeMemory()函数释放内存空间
        print('TODO: 调用FreeMemory()函数释放内存空间')
        pass
