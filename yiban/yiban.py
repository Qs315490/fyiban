#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor
# @Date: 2022-6-18
# 易班校本化 接口封装

import sys
sys.path.append("..")

from yiban.base import Base
from yiban.signin import SignIn
from yiban.submit import HealthSubmit


class Yiban(Base):
    def __init__(self, mobile:str, password:str) -> None:
        super().__init__()
        self._user_name      = ""  # 用户名
        self._user_token     = ""  # 登录密钥
        self._school_name    = ""  # 学校名
        self._school_faculty = ""  # 专业名

        self._user_info(mobile, password)

    def helath_submit(self, data:dict) -> str:
        # 健康打卡
        hs = HealthSubmit(self._user_token)

        if len(hs.get_task_uncompleted()) == 0:
            return f"{self._user_name}: 无未打卡任务 "
        try:
            hs.submit_task(data.copy())
            return f"{self._user_name}: 打卡成功 "
        except Exception as e:
            self._print(e)
            raise Exception(f"{self._user_name}: {e}")
    
    def uncompleted_task(self):
        return HealthSubmit(self._user_token).get_task_uncompleted()

    def _user_info(self, mobile:str, password:str):
        try:
            u = SignIn(mobile, password)
        except Exception as e:
            super()._print(e)
            super()._print(f"{mobile}: 登录失败")
            raise Exception(e)

        self._user_name      =  u.get_user_name()
        self._user_token     =  u.get_user_access_token()
        self._school_name    =  u.get_user_school_name()
        self._school_faculty =  u.get_user_school_faculty()

    def _print(self, msg: str) -> None:
        msg = f"{self._user_name}: {msg}"
        return super()._print(msg)


if __name__ == "__main__":
    mobile = ""
    password = ""
    yb = Yiban(mobile, password)
    print(yb.uncompleted_task())