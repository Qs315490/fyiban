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

from typing import AnyStr

class SchoolBasedAuth:
    def __init__(self, mobile: str, password: str) -> None :
        self.req = BaseReq()
        self.user_info = {}
        self.mobile = mobile
        self.password = password

        # Set auth requests headers and cookies
        self.req.session.headers.update(SchoolBased.headers())

        add_dict_to_cookiejar(
            self.req.session.cookies, SchoolBased.cookies())

    def _re_auth(self, verify: str) -> None:
        client_id = '95626fa3080300ea'
        redirect_uri = 'https://f.yiban.cn/iapp7463'

        self.req.get(
            url='https://api.uyiban.com/base/c/auth/yiban',
            params={
                'verifyRequest': verify, 
                'CSRF': SchoolBased.csrf()
            }
        )

        self.req.get(
            url='https://oauth.yiban.cn/code/html',
            params={
                'client_id': client_id, 
                'redirect_uri': redirect_uri
            }
        )

        self.req.post(
            url='https://oauth.yiban.cn/code/usersure',
            data={
                'client_id': client_id, 
                'redirect_uri': redirect_uri
            }
        )

    def _auth(self) -> None:
        "https://f.yiban.cn/iapp/index"
        "https://f.yiban.cn/iframe/index"

        login_res = self.req.get(
            url='https://oauth.yiban.cn/code/html?client_id=95626fa3080300ea&redirect_uri=https://f.yiban.cn/iapp7463'
        )
        rsa_key = login_res.text.split('id="key" value="')[1].split('"')[0]
        login_data = {
            'oauth_uname' : self.mobile,
            'oauth_upwd' : self.encrypt_rsa(self.password, rsa_key),
            'client_id' : '95626fa3080300ea',
            'redirect_uri' : 'https://f.yiban.cn/iapp7463'
        }
        login_res = self.req.post(
            url="https://oauth.yiban.cn/code/usersure",
            data=login_data
        )

        response = self.req.get(
            url='https://f.yiban.cn/iframe/index',
            params={'act': 'iapp7463'},
            allow_redirects=False
        )

        verify = findall(r"verify_request=(.*?)&", response.headers.get("Location"))[0]

        # re auth
        self._re_auth(verify)

        response = self.req.get(
            url='https://api.uyiban.com/base/c/auth/yiban',
            params={
                'verifyRequest': verify, 
                'CSRF': SchoolBased.csrf()
            },
        ).json()

        # if auth done return requests class else raise
        if response['code'] == 0:
            self.user_info = response['data']
            return self.req
        else:
            raise Exception(f"Auth Error {response['msg']}")

    def _get_name(self) -> AnyStr:
        return self.user_info['PersonName']

    @staticmethod
    def encrypt_rsa(data: str, rsa_key: str) -> AnyStr:
        """
        登录密码加密
        :param data: （必须）待加密密码
        :return: Any
        """
        data = bytes(data, encoding="utf8")
        encrypt = PKCS1_v1_5.new(RSA.importKey(rsa_key))
        sencrypt = b64encode(encrypt.encrypt(data))
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