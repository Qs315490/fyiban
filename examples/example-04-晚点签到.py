#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Moozae
# @Date: 2022-10-28

# 易班 校本化应用签到示例

from yiban import Yiban

yb = Yiban("账号", "密码")
sign_data='{"Reason":"","AttachmentFileName":"","LngLat":"学校坐标","Address":"xx省 xx市 xx区 xx路 xx号"}' # 学校坐标可通过高德开放平台 https://lbs.amap.com/tools/picker 获取
print(yb.submit_sign_feedback(sign_data)) # 校本化签到

