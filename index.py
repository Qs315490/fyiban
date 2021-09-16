import requests
import os

"""
获取环境变量
"""
env = {
  'YIBAN_MOBILE': 'YIBAN_MOBILE',  # 账号
  'YIBAN_PASSWORD': 'YIBAN_PASSWORD',  # 密码
  'BARK_PUSH': 'BARK_PUSH'  # Bark
}

if env['YIBAN_MOBILE'] in os.environ:
  mobile = os.getenv('YIBAN_MOBILE')
  print("已从环境变量中获取Mobile")

if env['YIBAN_PASSWORD'] in os.environ:
  password = os.getenv('YIBAN_PASSWORD')
  print("已从环境变量中获取Password")

if env['BARK_PUSH'] in os.environ:
  bark = os.getenv('BARK_PUSH')
  print("已从环境变量中获取Bark")


reqHeaders = {"Origin": "https://c.uyiban.com", "User-Agent": "Yiban-Pro", "AppVersion": "5.0"}

def getToken():
  """
  登录函数
  """
  try:
      url = f'https://mobile.yiban.cn/api/v4/passport/login?mobile={mobile}&password={password}&ct=2&identify=1'
      resp = requests.post(url,headers=reqHeaders).json()
      access_token = resp['data']['access_token']
      name = resp['data']['user']['name']
      print(access_token)
  except KeyError:
      raise 'Error: getToken'

getToken()