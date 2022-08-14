import logging

import TestConfig

from yiban import Yiban

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

yb = Yiban("", "")

# User
token = yb.get_user_access_token()
print(token)

# Task
name = yb.get_user_name() # 姓名
print(name)

school_name  = yb.get_user_school_name() # 院校名称
print(school_name)

uncompleted_task = yb.get_uncompleted_task() # 校本化未完成任务
print(uncompleted_task)

task = yb.get_completed_task() # 校本化完成任务
print(task)

