#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor
# @Date: 2022-10-25

""" SchoolBasedAuth Class """

from re import findall
from requests.utils import add_dict_to_cookiejar

from yiban.Core import BaseReq
from yiban.Core import SchoolBased

from base64 import b64encode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


class SchoolBasedAuth:
    def __init__(self, mobile: str, password: str) -> None:
        self.req = BaseReq()
        self.user_info = {}
        self.mobile = mobile
        self.password = password

        # Set auth requests headers and cookies
        self.req.session.headers.update(SchoolBased.headers())

        add_dict_to_cookiejar(self.req.session.cookies, SchoolBased.cookies())

    def _re_auth(self, verify: str) -> None:
        client_id = "95626fa3080300ea"
        redirect_uri = "https://f.yiban.cn/iapp7463"

        self.req.get(
            url="https://api.uyiban.com/base/c/auth/yiban",
            params={"verifyRequest": verify, "CSRF": SchoolBased.csrf()},
        )

        self.req.get(
            url="https://oauth.yiban.cn/code/html",
            params={"client_id": client_id, "redirect_uri": redirect_uri},
        )

        self.req.post(
            url="https://oauth.yiban.cn/code/usersure",
            data={"client_id": client_id, "redirect_uri": redirect_uri},
        )

    def _auth(self) -> BaseReq:
        "https://f.yiban.cn/iapp/index"
        "https://f.yiban.cn/iframe/index"

        # login_res = self.req.get(
        #     url='https://www.yiban.cn/login'
        # )
        # rsa_key = login_res.text.split("data-keys='")[1].split("'")[0]
        # key_time = login_res.text.split("data-keys-time='")[1].split("'")[0]
        # login_data = {
        #     'account' : self.mobile,
        #     'password' : self.encrypt_rsa(self.password, rsa_key),
        #     # 'captcha' : None,
        #     'keysTime' : key_time,
        #     # 'rid': ''
        #     # 'redirect_uri' : 'https://f.yiban.cn/iapp7463'
        # }
        # # TODO 验证码
        # login_res = self.req.post(
        #     url="https://www.yiban.cn/login/doLoginAjax",
        #     headers={

        #     },
        #     data=login_data
        # )

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
-----END PUBLIC KEY-----"""
        login_data = {
            "mobile": self.mobile,
            "password": self.encrypt_rsa(self.password, rsa_key),
            "ct": 2,
            "identify": 0,
        }

        login_res = self.req.post(
            url="https://m.yiban.cn/api/v4/passport/login",
            headers={"AppVersion": "5.1.2"},
            data=login_data,
        ).json()

        if login_res["response"] != 100:
            raise Exception(f"状态异常：{login_res['response']} {login_res['message']}")
        access_token = login_res["data"]["access_token"]
        response = self.req.get(
            url="https://f.yiban.cn/iapp/index",
            params={"act": "iapp7463"},
            headers={
                "authorization": "Bearer " + access_token,
                'logintoken': access_token,
            },
            allow_redirects=False,
        )

        location = response.headers.get("Location")
        assert location is not None
        verify = findall(r"verify_request=(.*?)&", location)[0]

        # re auth
        self._re_auth(verify)

        response = self.req.get(
            url="https://api.uyiban.com/base/c/auth/yiban",
            params={"verifyRequest": verify, "CSRF": SchoolBased.csrf()},
        ).json()

        # if auth done return requests class else raise
        if response["code"] == 0:
            self.user_info = response["data"]
            return self.req
        else:
            raise Exception(f"Auth Error {response['msg']}")

    def _get_name(self) -> str:
        return self.user_info["PersonName"]

    @staticmethod
    def encrypt_rsa(data: str, rsa_key: str) -> str:
        """
        登录密码加密
        :param data: （必须）待加密密码
        :return: Any
        """
        data_bytes = bytes(data, encoding="utf8")
        encrypt = PKCS1_v1_5.new(RSA.importKey(rsa_key))
        sencrypt = b64encode(encrypt.encrypt(data_bytes))
        return sencrypt.decode("utf-8")


"""
{
'code': 0, 
'msg': '', 
'data': {
    'UniversityName': '', 
    'UniversityId': '', 
    'PersonId': '', 
    'PersonName': '', 
    'State': 1, 
    'PersonType': 'student', 
    'UniversityIcon': '', 
    'Container': 'StudentDefault', 
    'HomeTheme': 'HomeDefault', 
    'CustomApps': {
        'up': [], 
        'down': []}, 
        'Group': [], 
        'Apps': [
            {
                'Id': '', 
                'ServiceId': '', 
                'AppIcon': '', 
                'AppUrl': '', 
                'AppRuleUrl': '', 
                'AuthCode': '', 
                'AppName': ''
            }
        ], 
        'WxState': 0, 
        'DingDingState': 0
    }
}
"""
