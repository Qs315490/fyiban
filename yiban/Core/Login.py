from base64 import b64encode
from typing import Dict, AnyStr

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


from yiban.Core import BaseYiban

"""
登录接口返回信息
{
    'response': 100, 
    'message': '请求成功', 
    'is_mock': False, 
    'data': {
        'access_token': '',
        'user': {
            'sex': '1', 
            'name': '姓名', 
            'nick': '昵称', 
            'user_id': int, 
            'phone': '电话号码', 
            'authority': '1', 
            'isSchoolVerify': True, 
            'school': {
                'isVerified': True, 
                'schoolName': '', 
                'schoolId': int, 
                'schoolOrgId': int, 
                'collegeName': '专业', 
                'collegeId': int, 
                'className': '', 
                'classId': 0, 
                'joinSchoolYear': '2020', 
                'type': 1
            }
        },
    }
}
"""


class Login(BaseYiban):
    def __init__(self):
        super().__init__()

    def get_user_info(self, mobile: str, password: str) -> Dict:
        """ Login function """
        response = self.post(
            url="https://mobile.yiban.cn/api/v4/passport/login",
            headers={"User-Agent": "Yiban", "AppVersion": "5.0"},
            data={
                'ct': '2',
                'identify': '1',
                'mobile': mobile,
                'password': self.encrypt_rsa(password)}
        ).json()

        self._log(f"Login Response {response}", 10)

        if response['response'] == 100:
            return response['data']

    @staticmethod
    def encrypt_rsa(data: str) -> AnyStr:
        """
        登录密码加密
        :param data: （必须）待加密密码
        :return: Any
        """
        rsa_key = """-----BEGIN PUBLIC KEY-----
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
            """
        data = bytes(data, encoding="utf8")
        encrypt = PKCS1_v1_5.new(RSA.importKey(rsa_key))
        sencrypt = b64encode(encrypt.encrypt(data))
        return sencrypt.decode("utf-8")
