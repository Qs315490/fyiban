""" 校本化分应用 认证"""
from logging import log
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from typing import Dict, AnyStr, Any


class SchoolBased:
    @staticmethod
    def csrf() -> AnyStr:  
        return '00000'

    @staticmethod
    def headers() -> Dict: 
        return { "Origin": "https://c.uyiban.com", "User-Agent": "Yiban", "AppVersion": "5.0" }

    @staticmethod
    def cookies(access_token) -> Dict: 
        return { "yiban_user_token": access_token, "loginToken": access_token, "csrf_token": "00000" }

    @staticmethod
    def _log(msg: str = None, level: int = 20) -> None:
        msg = f"Yiban {msg}"
        log(msg=msg, level=level)

    @staticmethod
    def aes_encrypt(data: Any) -> AnyStr:
        """
        提交表单加密
        :param data: （必须）提交表单数据
        :return: AnyStr
        """
        aes_key = '2knV5VGRTScU7pOq'
        aes_iv = 'UmNWaNtM0PUdtFCs'
        aes_key = bytes(aes_key, 'utf-8')
        aes_iv = bytes(aes_iv, 'utf-8')
        data = bytes(data, 'utf-8')
        bs = AES.block_size
        padding = bs - len(data) % bs
        padding_text = bytes(chr(padding) * padding, 'utf-8')
        data = data + padding_text
        cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
        encrypted = b64encode(cipher.encrypt(data))
        return b64encode(encrypted)

    @staticmethod
    def aes_decrypt(data: Any) -> AnyStr:
        """
        提交表单解密
        :param data: （必须）提交表单加密数据
        :return: AnyStr
        """
        aes_key = '2knV5VGRTScU7pOq'
        aes_iv = 'UmNWaNtM0PUdtFCs'
        aes_key = bytes(aes_key, 'utf-8')
        aes_iv = bytes(aes_iv, 'utf-8')
        data = b64decode(b64decode(data))
        cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
        decrypted = cipher.decrypt(data)
        return decrypted.decode('Utf-8')
