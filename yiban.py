import re
import json
import time
import base64
import requests
import datetime
from urllib import parse
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

CSRF = '000000'
COOKIE = {'csrf_token': CSRF}
HEADERS = {
  "Origin": "https://c.uyiban.com", 
  "User-Agent": "Yiban-Pro", 
  "AppVersion": "5.0"
}


class Yiban():
  def __init__(self, mobile, password, data, extend) -> None:
    self.mobile = mobile
    self.password = password
    self.data = data
    self.extend = extend
    self.session = requests.session()
    self.access_token = ''

  def main(self):
    try:
      self.getToken()
      self.getAuth()
      return self.doSubmit()
    except KeyError:
      return "Error"

  def req(self, url, method='get',data=None, cookies=None, allow_redirects=True):
    """
    构造请求函数
    """
    if method == 'get':
      return self.session.get(url, params=data, cookies=cookies, headers=HEADERS, allow_redirects=allow_redirects, timeout=10)
    else:
      return self.session.post(url, data=data, cookies=cookies, headers=HEADERS, allow_redirects=allow_redirects, timeout=10)

  def getToken(self):
    """
    登录函数
    获取access_token
    """
    url = f'https://mobile.yiban.cn/api/v4/passport/login?mobile={self.mobile}&password={doCrypto(self.password)}&ct=2&identify=1'
    resp = self.req(url, method='post').json()
    self.access_token = resp['data']['access_token']

  def getAuth(self):
    """用户认证"""
    """Verify"""
    url = 'http://f.yiban.cn/iapp/index?act=iapp7463'  # 校本化iapp7463
    resp = self.req(url, cookies={'loginToken': self.access_token}, allow_redirects=False)
    verify = re.findall(r"verify_request=(.*?)&", resp.headers.get("Location"))[0]  # 正则verify

    """Auth"""
    url = f'https://api.uyiban.com/base/c/auth/yiban?verifyRequest={verify}&CSRF={CSRF}'
    resp = self.req(url, cookies=COOKIE).json()

    """
    重认证
    """
    url = 'https://oauth.yiban.cn/code/usersure'
    data = {
      'client_id': '95626fa3080300ea',
      'redirect_uri': 'https://f.yiban.cn/iapp7463'
    }
    resp = self.req(url, data=data, method='post')

  def doSubmit(self):
    """
    打卡提交
    """
    url = f'https://api.uyiban.com/officeTask/client/index/uncompletedList?StartTime={getStartTime()}&EndTime={getEndTime()}&CSRF={CSRF}'
    resp = self.req(url, cookies=COOKIE).json()
    if resp['data'] == []:
      return "无未打卡信息"
    else:
      for i in resp['data']:
        if i['Title'] == '每日学生疫情上报':
          TaskId = i['TaskId']
          self.extend['TaskId'] = TaskId

          url = f'https://api.uyiban.com/officeTask/client/index/detail?TaskId={TaskId}&CSRF={CSRF}'
          WFId = self.req(url, cookies=COOKIE).json()['data']['WFId']
          data = json.dumps(self.data, ensure_ascii=False)
          extend = json.dumps(self.extend, ensure_ascii=False)

          url = f'https://api.uyiban.com/workFlow/c/my/apply/{WFId}?CSRF={CSRF}'
          data = {
              'data': data,
              'extend': extend,
          }
          resp = self.req(url, method='post', data=data, cookies=COOKIE).json()
          if resp['code'] == 0:
              return "打卡成功"
          else:
              return 'Error: doSubmit'
      return 'Error: TaskId'


def doCrypto(password):
    """
    加密
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


def getEndTime():
    return time.strftime("%Y-%m-%d 23:59", time.localtime())

def getStartTime():
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=-14)
    n_days = now + delta
    return n_days.strftime('%Y-%m-%d')