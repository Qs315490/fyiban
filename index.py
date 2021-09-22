import os
import json
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
from yiban import Yiban

"""
环境变量参数
"""
ENV = {
  'YIBAN_NAME': 'YIBAN_NAME',
  'YIBAN_MOBILE': 'YIBAN_MOBILE',  # 账号
  'YIBAN_PASSWORD': 'YIBAN_PASSWORD',  # 密码
  'YIBAN_DATA': 'YIBAN_DATA',  # 提交表单1
  'YIBAN_EXTEND': 'YIBAN_DEXTEND',  # 提交表单2
  'DD_BOT_TOKEN': 'DD_BOT_TOKEN',  # 钉钉推送
  'DD_BOT_SECRET': 'DD_BOT_SECRET',  # 钉钉推送密钥
  'BARK_PUSH': 'BARK_PUSH'  # Bark
}

"""
尝试从配置文件获取账号信息
优先级：配置文件 -> 环境变量
配置文件适用多人打卡
"""

def main():
  name = ''
  mobile = ''
  password = ''
  msg = ''
  title = f'{time.strftime("%m-%d", time.localtime())}易班打卡'

  try:
    with open('./config.json', 'rb') as f:
      config = json.load(f)
    data = config['data']
    extend = config['extend']
  except:
    raise "配置文件有误"

  for i in config['user']:
    name = i['name']
    mobile = i['mobile']
    password = i['password']
    if mobile == '' or password == '':
      break
    else:
      print("正在从配置文件启动打卡")
      result = name + Yiban(mobile, password, data, extend).main()
      msg = msg + '\n' + result
      return title + msg

  if ENV['YIBAN_NAME'] in os.environ:
    name = os.getenv('YIBAN_NAME')
    print("已从环境变量中获取name")
    
  if ENV['YIBAN_MOBILE'] in os.environ:
    mobile = os.getenv('YIBAN_MOBILE')
    print("已从环境变量中获取mobile")
  else:
    raise "账号为空"

  if ENV['YIBAN_PASSWORD'] in os.environ:
    password = os.getenv('YIBAN_PASSWORD')
    print("已从环境变量中获取password")
  else:
    raise "密码为空"

  if ENV['YIBAN_DATA'] in os.environ:
    data = json.loads(os.getenv('YIBAN_DATA'))
    print("已从环境变量中获取data")

  if ENV['YIBAN_EXTEND'] in os.environ:
    extend = json.loads(os.getenv('YIBAN_EXTEND'))
    print("已从环境变量中获取extend")

  result = name + Yiban(mobile, password, data, extend).main()
  msg = msg + '\n' + result
  return msg


def dingPush(token, secret, title, msg):
  timestamp = str(round(time.time() * 1000))
  secret_enc = secret.encode('utf-8')
  string_to_sign = f'{timestamp}\n{secret}'
  string_to_sign_enc = string_to_sign.encode('utf-8')
  hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
  sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
  url = f'https://oapi.dingtalk.com/robot/send?access_token={token}&timestamp={timestamp}&sign={sign}'
  data = {
    "msgtype": "markdown",
    "markdown": {
        "title": title,
        "text": f'### {time.strftime("%m-%d", time.localtime())} 易班打卡 \n {msg}'
    }
  }
  requests.post(url, data=json.dumps(data), headers={
    "Content-Type": "application/json",
    "Charset": "UTF-8"
  })


if __name__ == '__main__':
  msg = main()
  title = f'{time.strftime("%m-%d", time.localtime())}易班打卡'
  print(msg)
  if ENV['BARK_PUSH'] in os.environ:
    bark = os.getenv('BARK_PUSH')
    print("已从环境变量中获取bark")
    requests.post(url=f'https://api.day.app/{bark}/{title + msg}')
    print("bark推送成功")
  
  if ENV['DD_BOT_TOKEN'] in os.environ:
    if ENV['DD_BOT_SECRET'] in os.environ:
      token = os.getenv('DD_BOT_TOKEN')
      secret = os.getenv('DD_BOT_SECRET')
      dingPush(token, secret, title, msg)
      print("钉钉推送成功")
