""" school based auth """
from re import findall
from requests.utils import add_dict_to_cookiejar

from yiban.Core import BaseReq
from yiban.Core import SchoolBased


class SchoolBasedAuth:
    def __init__(self, access_token: str) -> None :
        self.req = BaseReq()

        # Set auth requests headers and cookies
        self.req.session.headers.update(SchoolBased.headers())

        add_dict_to_cookiejar(
            self.req.session.cookies, SchoolBased.cookies(access_token))

    def _re_auth(self, verify: str) -> None:
        client_id = '95626fa3080300ea'
        redirect_uri = 'https://f.yiban.cn/iapp7463'

        self.req.get(
            url='https://api.uyiban.com/base/c/auth/yiban',
            params={
                'verifyRequest': verify, 
                'CSRF': SchoolBased.csrf()
            }
        )

        self.req.get(
            url='https://oauth.yiban.cn/code/html',
            params={
                'client_id': client_id, 
                'redirect_uri': redirect_uri
            }
        )

        self.req.post(
            url='https://oauth.yiban.cn/code/usersure',
            data={
                'client_id': client_id, 
                'redirect_uri': redirect_uri
            }
        )

    def _auth(self) -> None:
        "https://f.yiban.cn/iapp/index"
        "https://f.yiban.cn/iframe/index"

        response = self.req.get(
            url='https://f.yiban.cn/iframe/index',
            params={'act': 'iapp7463'},
            allow_redirects=False
        )

        verify = findall(r"verify_request=(.*?)&", response.headers.get("Location"))[0]

        # re auth
        self._re_auth(verify)

        response = self.req.get(
            url='https://api.uyiban.com/base/c/auth/yiban',
            params={
                'verifyRequest': verify, 
                'CSRF': SchoolBased.csrf()
            },
        ).json()

        # if auth done return requests class else raise
        if response['code'] == 0:
            self.user_info = response['data']
            return self.req
        else:
            raise Exception(f"Auth Error {response['msg']}")