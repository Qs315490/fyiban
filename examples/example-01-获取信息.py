#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor
# @Date: 2022-6-26

# 易班 获取信息示例

import logging
from yiban import Yiban

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO) # DEBUG

yb = Yiban("账号", "密码")              # 传入账号密码 实例化 Yiban
name = yb.get_user_name()               # 获取用户名
token = yb.get_user_access_token()      # 获取登录密钥
task_list = yb.get_uncompleted_task()   # 获取校本化应用中 未完成的任务
task_completed_list = yb.get_completed_task()  # 

