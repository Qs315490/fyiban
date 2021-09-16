import requests
import os
import base64
from urllib import parse
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
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
  print("已从环境变量中获取mobile")

if env['YIBAN_PASSWORD'] in os.environ:
  password = os.getenv('YIBAN_PASSWORD')
  print("已从环境变量中获取password")

if env['BARK_PUSH'] in os.environ:
  bark = os.getenv('BARK_PUSH')
  print("已从环境变量中获取bark")


reqHeaders = {"Origin": "https://c.uyiban.com", "User-Agent": "Yiban-Pro", "AppVersion": "5.0"}

def getToken():
  """
  登录函数
  """
  url = f'https://mobile.yiban.cn/api/v4/passport/login?mobile={mobile}&password={doCrypto(password)}&ct=2&identify=1'
  resp = requests.post(url,headers=reqHeaders).json()
  print(resp)

def doCrypto(password):
    """
    v4接口
    密码加密
    Rsa,base64
    """
    PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
    MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA6aTDM8BhCS8O0wlx2KzA
    Ajffez4G4A/QSnn1ZDuvLRbKBHm0vVBtBhD03QUnnHXvqigsOOwr4onUeNljegIC
    XC9h5exLFidQVB58MBjItMA81YVlZKBY9zth1neHeRTWlFTCx+WasvbS0HuYpF8+
    KPl7LJPjtI4XAAOLBntQGnPwCX2Ff/LgwqkZbOrHHkN444iLmViCXxNUDUMUR9bP
    A9/I5kwfyZ/mM5m8+IPhSXZ0f2uw1WLov1P4aeKkaaKCf5eL3n7/2vgq7kw2qSmR
    AGBZzW45PsjOEvygXFOy2n7AXL9nHogDiMdbe4aY2VT70sl0ccc4uvVOvVBMinOp
    d2rEpX0/8YE0dRXxukrM7i+r6lWy1lSKbP+0tQxQHNa/Cjg5W3uU+W9YmNUFc1w/
    7QT4SZrnRBEo++Xf9D3YNaOCFZXhy63IpY4eTQCJFQcXdnRbTXEdC3CtWNd7SV/h
    mfJYekb3GEV+10xLOvpe/+tCTeCDpFDJP6UuzLXBBADL2oV3D56hYlOlscjBokNU
    AYYlWgfwA91NjDsWW9mwapm/eLs4FNyH0JcMFTWH9dnl8B7PCUra/Lg/IVv6HkFE
    uCL7hVXGMbw2BZuCIC2VG1ZQ6QD64X8g5zL+HDsusQDbEJV2ZtojalTIjpxMksbR
    ZRsH+P3+NNOZOEwUdjJUAx8CAwEAAQ==
    -----END PUBLIC KEY-----
    '''
    encrypt = PKCS1_v1_5.new(RSA.importKey(PUBLIC_KEY))
    Sencrypt = base64.b64encode(encrypt.encrypt(bytes(password, encoding="utf8")))
    return parse.quote(Sencrypt.decode("utf-8"))
getToken()