#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor
# @Date: 2022-10-25

""" Login Class """

from base64 import b64encode
from typing import Dict, AnyStr

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

from yiban.Core import BaseReq

class Login:
    def __init__(self):
        self.req = BaseReq()

    def get_user_info(self, mobile: str, password: str) -> Dict:
        """ Login function """
        # 暂时弃用
        # response = self.post(
        #     url="https://mobile.yiban.cn/api/v4/passport/login",
        #     headers={"User-Agent": "Yiban", "AppVersion": "5.0"},
        #     data={
        #         'ct': '2',
        #         'identify': '1',
        #         'mobile': mobile,
        #         'password': self.encrypt_rsa(password)}
        # ).json()

        # self._log(f"Login Response {response}", 10)

        # if response['response'] == 100:
        #     return response['data']

    def get_user_access_token(self, mobile: str, password: str) -> str:
        response = self.req.post(
            url="https://www.yiban.cn/login/doLoginAjax",
            headers={"User-Agent": "Yiban", "AppVersion": "5.0"},
            data={
                'account': mobile,
                'password': password
            }
        )
        try:
            access_token = response.cookies.get_dict()['yiban_user_token']
            return access_token
        except Exception as e:
            print(f"Login Error: {e} ")
        
        
    @staticmethod
    def encrypt_rsa(data: str) -> AnyStr:
        """
        登录密码加密
        :param data: （必须）待加密密码
        :return: Any
        """
        rsa_key = """-----BEGIN PUBLIC KEY-----
            MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCnslKgSPbbGTy1p5pAknnVT2sr
            58YNWGrHR/0TOF9HneSyQDubc7QaXwmbHlRtYqr/jcaQ+0PDRHcVdaHCLEcEm7U3
            RaiZNP38vgYMTlKak5eywfcXBkvGhlGHJ6QVEGsPDsxKqCR8DX3malgfOw0wnkBV
            dA5Xc8xsf+cydAbWDQIDAQAB
            -----END PUBLIC KEY-----
            """
        data = bytes(data, encoding="utf8")
        encrypt = PKCS1_v1_5.new(RSA.importKey(rsa_key))
        sencrypt = b64encode(encrypt.encrypt(data))
        return sencrypt.decode("utf-8")

"""
登录接口返回信息
{
    'response': 100, 
    'message': '请求成功', 
    'is_mock': False, 
    'data': {
        'access_token': '',
        'user': {
            'sex': '1', 
            'name': '姓名', 
            'nick': '昵称', 
            'user_id': int, 
            'phone': '电话号码', 
            'authority': '1', 
            'isSchoolVerify': True, 
            'school': {
                'isVerified': True, 
                'schoolName': '', 
                'schoolId': int, 
                'schoolOrgId': int, 
                'collegeName': '专业', 
                'collegeId': int, 
                'className': '', 
                'classId': 0, 
                'joinSchoolYear': '2020', 
                'type': 1
            }
        },
    }
}
"""