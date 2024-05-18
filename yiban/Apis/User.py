#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor
# @Date: 2022-10-25

""" User Class """

from yiban.Core import SchoolBasedAuth
from yiban.Core.Login import Login

class User:
    def __init__(self, mobile: str, password: str):
        self.__mobile = mobile
        self.__password = password
        login = Login()
        self.user = login.get_user_info(self.__mobile, self.__password)
        self.__access_token = login.get_user_access_token(mobile, password)

    def get_user_access_token(self) -> str:
        """获取用户登录密钥"""
        return self.__access_token

    def get_user_name(self) -> str:
        """获取用户名"""
        return self.user['name']

    def get_user_phone(self) -> str:
        """获取用户手机号"""
        return self.user['phone']

    def get_user_school_name(self) -> str:
        """获取用户学校名称"""
        return self.user['school']['schoolName']
