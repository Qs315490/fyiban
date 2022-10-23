#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor
# @Date: 2022-6-26

# 易班 校本化应用打卡示例

import logging
from yiban import Yiban

# 此处需要手动抓包 解密 修改
# 格式 需包含 Data 及 Extend

task_data = {
    "WFId": "",
    "Data": {
        "9843754e97aad058523524bdb8991bcd": "",
        "72fe9c2c81a48fd0968edbbb3f2c1c42": "",
        "769bbfbfb026629f1ddb0294a9c0d257": "",
        "90b5b83950ae456fefebb0f751406e2d": [],
        "0242914b8746275c5073ccdb156f9d1d": [],
        "1bac180dd37455f7c16a36336c0411a8": {
            "time": "2022-05-20 00:00",
            "longitude": 0,
            "latitude": 0,
            "address": ""
        }
    },

    "Extend": {
        "TaskId": "",
        "title": "任务信息",
        "content": [
            {"label": "任务名称", "value": ""},
            {"label": "发布机构", "value": ""},
            {"label": "发布人", "value": ""}
        ]
    }
}

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO) # DEBUG

yb = Yiban("账号", "密码")
yb.submit_task_feedback(task_data) # 校本化打卡

