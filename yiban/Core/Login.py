#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor
# @Date: 2022-10-25

""" Login Class """

from base64 import b64encode

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

from yiban.Core import BaseReq

from logging import log


class Login:
    def __init__(self):
        self.req = BaseReq()
        self.access_token = ""

    def get_user_info(self, mobile: str, password: str) -> dict:
        """Login function"""
        response = self.req.post(
            url="https://m.yiban.cn/api/v4/passport/login",
            headers={"User-Agent": "Yiban", "AppVersion": "5.1.2"},
            data={
                "ct": "2",
                "identify": "1",
                "mobile": mobile,
                "password": self.encrypt_rsa(password),
            },
        ).json()

        log(10,f"Login Response {response}")

        if response["response"] == 100:
            self.access_token = response["data"]["access_token"]
            self.req.session.cookies.set("loginToken", self.access_token)
            return response["data"]["user"]
        raise Exception(f"登录失败：{response['message']}")

    def get_user_access_token(self, mobile: str, password: str) -> str:
        # response = self.req.post(
        #     url="https://www.yiban.cn/login/doLoginAjax",
        #     headers={"User-Agent": "Yiban", "AppVersion": "5.1.0"},
        #     data={"account": mobile, "password": password},
        # )
        # try:
        #     access_token = response.cookies.get_dict()["yiban_user_token"]
        #     return access_token
        # except Exception as e:
        #     print(f"Login Error: {e} ")
        if self.access_token == "":
            self.get_user_info(mobile, password)
        return self.access_token

    @staticmethod
    def encrypt_rsa(data: str) -> str:
        """
        登录密码加密
        :param data: （必须）待加密密码
        :return: Any
        """
        rsa_key = """-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAzq0rgsM++ZxLRGHpdfre
Hu6UXhdlUS5P2WOxRG14qU8/iWSb/CkOqgOl8AGcOhlthkvolCdpUvVcVsVUxBv0
YRN0Jb64zPrn5aLVwQT4RJn5tXvoqLdHIXis7pljXAMDPVZOVlWJkDMk8YU6HDaA
MqsD6l5p9lg2LMP4OhMgaPX+CkO370LB5vRjJTHp03n+IqfxXoC7DEd+kxRIEM2C
EDgUSYDJBDgwBvGALZmvB/a1b0im9t1P/EmnuE7uN9NRFoWyVpOiEwo/Ti7rmJGf
qNT3vvtfWo4nXsm1rYQXsPayoKDSRaba3gFY/1SYWLAuSO2q2da5ZCcsAk5RKy0V
c1hUg8n6y0YLAvuzoXY5VyNMXkhH5Zc5Kg64b5RxILeZpZG0MV7GFY3sw//k7SNg
darKT8A0Iv3l3lfguX3HNi6dkf97kS/EiA0tbkIB/JNjv13mq8HL7LijRt2hkKqP
PhQW88xC/exZilU5pAavoZOPuZIOTUHqtpRq4ZeKl+wDf+e5lPYFDpihWGjplGpa
4BOSmGeo/SyVFPji9QF4Pk0DRJF/NjwJoAC60xHAVt5Z4gQSOOOjNZDCswA0ry2L
e8m5cv5vPGY75uVrGqALQ6Xm961PPc5cJ1q7tmEZMj+z5HE7tgAdhiPI6acKgrAv
+1k4N0OVqKamMS+PVpD05hUCAwEAAQ==
-----END PUBLIC KEY-----
            """
        data_bytes = bytes(data, encoding="utf8")
        encrypt = PKCS1_v1_5.new(RSA.importKey(rsa_key))
        sencrypt = b64encode(encrypt.encrypt(data_bytes))
        return sencrypt.decode("utf-8")


# 登录接口返回信息
# {
#     'response': 100,
#     'message': '请求成功',
#     'is_mock': False,
#     'data': {
#         'access_token': '',
#         'user': {
#             'sex': '1',
#             'name': '姓名',
#             'nick': '昵称',
#             'user_id': int,
#             'phone': '电话号码',
#             'authority': '1',
#             'isSchoolVerify': True,
#             'school': {
#                 'isVerified': True,
#                 'schoolName': '',
#                 'schoolId': int,
#                 'schoolOrgId': int,
#                 'collegeName': '专业',
#                 'collegeId': int,
#                 'className': '',
#                 'classId': 0,
#                 'joinSchoolYear': '2020',
#                 'type': 1
#             }
#         },
#     }
# }
