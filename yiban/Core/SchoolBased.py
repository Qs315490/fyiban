#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor
# @Date: 2022-10-25

""" SchoolBased Class """

from logging import log
from Crypto.Cipher import AES
from base64 import b64encode, b64decode


class SchoolBased:
    @staticmethod
    def csrf() -> str:
        return "00000"

    @staticmethod
    def headers() -> dict:
        return {
            "Origin": "https://c.uyiban.com",
            "User-Agent": "Yiban",
            "AppVersion": "5.1.2",
        }

    @staticmethod
    def cookies() -> dict:
        return {"csrf_token": "00000"}

    @staticmethod
    def _log(msg: str = "", level: int = 20) -> None:
        msg = f"Yiban {msg}"
        log(msg=msg, level=level)

    @staticmethod
    def aes_encrypt(data: str) -> str:
        """
        提交表单加密
        :param data: （必须）提交表单数据
        :return: str
        """
        aes_key = "2knV5VGRTScU7pOq"
        aes_iv = "UmNWaNtM0PUdtFCs"
        aes_key = bytes(aes_key, "utf-8")
        aes_iv = bytes(aes_iv, "utf-8")
        data_bytes = bytes(data, "utf-8")
        bs = AES.block_size
        padding = bs - len(data_bytes) % bs
        padding_text = bytes(chr(padding) * padding, "utf-8")
        data_bytes = data_bytes + padding_text
        cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
        encrypted = b64encode(cipher.encrypt(data_bytes))
        return b64encode(encrypted).decode("utf-8")

    @staticmethod
    def aes_decrypt(data: str) -> str:
        """
        提交表单解密
        :param data: （必须）提交表单加密数据
        :return: str
        """
        aes_key = "2knV5VGRTScU7pOq"
        aes_iv = "UmNWaNtM0PUdtFCs"
        aes_key = bytes(aes_key, "utf-8")
        aes_iv = bytes(aes_iv, "utf-8")
        data_b64 = b64decode(b64decode(data))
        cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
        decrypted = cipher.decrypt(data_b64)
        return decrypted.decode("Utf-8")
