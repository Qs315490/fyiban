#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor
# @Date: 2022-10-25

""" Yiban Class """

from yiban.Apis import User
from yiban.Apis import Task


class Yiban(
    User,
    Task,
):
    def __init__(
            self,
            mobile:   str,
            password: str,
    ):
        """
        易班 Python API service
        :param mobile:   (必须) 用户账号
        :param password: (必须) 用户密码
        """
        super().__init__(mobile=mobile, password=password)  # init User
        super(User, self).__init__(mobile=mobile, password=password)  # init Task
        # try:
        #     super(User, self).__init__(mobile=mobile, password=password)  # init Task
        # except:
        #     pass