import os
import json
import time
import requests
from yiban import Yiban

"""
环境变量参数
"""
ENV = {
  'YIBAN_NAME': 'YIBAN_NAME',
  'YIBAN_MOBILE': 'YIBAN_MOBILE',  # 账号
  'YIBAN_PASSWORD': 'YIBAN_PASSWORD',  # 密码
  'BARK_PUSH': 'BARK_PUSH'  # Bark
}

"""
尝试从配置文件获取账号信息
优先级：配置文件 > 环境变量
配置文件适用多人打卡
"""

name = ''
mobile = ''
password = ''
data = ''
extend = ''
bark = ''

try:
  with open('./config.json', 'rb') as f:
    config = json.load(f)
  data = config['data']
  extend = config['extend']
  for i in config['user']:
    name = i['name']
    mobile = i['mobile']
    password = i['password']
except:
  raise "配置文件有误"

if name == '':
  if ENV['YIBAN_NAME'] in os.environ:
    name = os.getenv('YIBAN_NAME')
    print("已从环境变量中获取name")
    
if mobile == '':
  if ENV['YIBAN_MOBILE'] in os.environ:
    mobile = os.getenv('YIBAN_MOBILE')
    print("已从环境变量中获取mobile")
  else:
    raise "账号为空"

if password == '':
  if ENV['YIBAN_PASSWORD'] in os.environ:
    password = os.getenv('YIBAN_PASSWORD')
    print("已从环境变量中获取password")
  else:
    raise "密码为空"

if ENV['BARK_PUSH'] in os.environ:
  bark = os.getenv('BARK_PUSH')
  print("已从环境变量中获取bark")

title = time.strftime("%m-%d", time.localtime()) + '易班打卡:\n'
result = name + Yiban(mobile, password, data, extend).main()
msg = title + "："+ result

if (bark != ''):
  requests.post(url=f'https://api.day.app/{bark}/{msg}')

print(msg)
