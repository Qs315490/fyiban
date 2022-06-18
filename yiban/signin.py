#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor
# @Date: 2022-4-20
# 易班登录

import sys
from requests import post
from base64 import b64encode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

sys.path.append("..")

from yiban.base import Base


class SignIn(Base):
    def __init__(self, mobile: str, password: str) -> None: self.__user_information = self.__sign_in(mobile, password)
    def get_user_id(self)             -> int: return self.__user_information["data"]["user"]["user_id"]                  # 用户ID
    def get_user_name(self)           -> str: return self.__user_information["data"]["user"]["name"]                     # 用户名称
    def get_user_phone(self)          -> str: return self.__user_information["data"]["user"]["phone"]                    # 用户电话
    def get_user_access_token(self)   -> str: return self.__user_information["data"]["access_token"]                     # 登录密钥
    def get_user_school_name(self)    -> str: return self.__user_information["data"]["user"]["school"]["schoolName"]     # 用户学校
    def get_user_school_faculty(self) -> str: return self.__user_information["data"]["user"]["school"]["collegeName"]    # 专业名称
    def get_user_join_year(self)      -> str: return self.__user_information["data"]["user"]["school"]["joinSchoolYear"] # 入学年份

    def __sign_in(self, mobile:str, password:str) -> dict:
        self._debug_msg("Class SignIn: __sigin_in")

        # 获取响应体
        response = post(
            url = 'https://mobile.yiban.cn/api/v4/passport/login',
            data = {
                'ct'       : '2',
                'identify' : '1',
                'mobile'   : mobile,
                'password' : self.__encrypt_rsa(password)},
            headers = {
                "Origin": "https://c.uyiban.com", 
                "User-Agent": "Yiban", 
                "AppVersion": "5.0"}
        ).json()
        
        self._debug_msg(response) # DEBUG

        if response["response"] == 100: 
            self._log_msg(f"Sign in successful. ")
            return response
        else: 
            self._err_msg(f"Sign in failed. ")
            raise Exception (response["message"])

    def __encrypt_rsa(self, data:str) -> str:
        # 登录加密
        rsa_key = '''-----BEGIN PUBLIC KEY-----
            MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA6aTDM8BhCS8O0wlx2KzA
            Ajffez4G4A/QSnn1ZDuvLRbKBHm0vVBtBhD03QUnnHXvqigsOOwr4onUeNljegIC
            XC9h5exLFidQVB58MBjItMA81YVlZKBY9zth1neHeRTWlFTCx+WasvbS0HuYpF8+
            KPl7LJPjtI4XAAOLBntQGnPwCX2Ff/LgwqkZbOrHHkN444iLmViCXxNUDUMUR9bP
            A9/I5kwfyZ/mM5m8+IPhSXZ0f2uw1WLov1P4aeKkaaKCf5eL3n7/2vgq7kw2qSmR
            AGBZzW45PsjOEvygXFOy2n7AXL9nHogDiMdbe4aY2VT70sl0ccc4uvVOvVBMinOp
            d2rEpX0/8YE0dRXxukrM7i+r6lWy1lSKbP+0tQxQHNa/Cjg5W3uU+W9YmNUFc1w/
            7QT4SZrnRBEo++Xf9D3YNaOCFZXhy63IpY4eTQCJFQcXdnRbTXEdC3CtWNd7SV/h
            mfJYekb3GEV+10xLOvpe/+tCTeCDpFDJP6UuzLXBBADL2oV3D56hYlOlscjBokNU
            AYYlWgfwA91NjDsWW9mwapm/eLs4FNyH0JcMFTWH9dnl8B7PCUra/Lg/IVv6HkFE
            uCL7hVXGMbw2BZuCIC2VG1ZQ6QD64X8g5zL+HDsusQDbEJV2ZtojalTIjpxMksbR
            ZRsH+P3+NNOZOEwUdjJUAx8CAwEAAQ==
            -----END PUBLIC KEY-----
            '''
        data = bytes(data, encoding="utf8") 
        encrypt = PKCS1_v1_5.new(RSA.importKey(rsa_key))
        sencrypt = b64encode(encrypt.encrypt(data))
        return sencrypt.decode("utf-8")


if __name__ == "__main__":
    a = SignIn("", "")
    print(a.get_user_access_token())

    """
    登录接口返回信息：

    {
        'response': 100,
        'message': '请求成功',
        'is_mock': False,
        'data': {
            'user': {
                'sex': '1',
                'name': '',
                'nick': '',
                'pic': {'s': '', 'm': '', 'b': '', 'o': ''},
                'user_id': 0,
                'phone': '',
                'authority': '1',
                'isSchoolVerify': True,
                'school': {
                    'isVerified': True,
                    'schoolName': '',
                    'schoolId': 0,
                    'schoolOrgId': 0,
                    'collegeName': '',
                    'collegeId': 0,
                    'className': '',
                    'classId': 0,
                    'joinSchoolYear': '',
                    'type': 1
                }
            },
            'access_token': ''
        }
    }
    """