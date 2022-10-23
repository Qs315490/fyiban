import requests

from typing import Dict

class BaseReq:
    def __init__(self):
        self.session = requests.session()

    def request(
            self, 
            method:  str, 
            url:     str, 
            params:  Dict = None,
            headers: Dict = None,
            cookies: Dict = None,
            data:    Dict = None, 
            body:    Dict = None,
            allow_redirects: bool = True
    ) -> requests.Response:
        
        """统一请求方法"""
        # 删除值为None的键
        if body is not None:
            body = {k: v for k, v in body.items() if v is not None}

        if data is not None and isinstance(data, dict):
            data = {k: v for k, v in data.items() if v is not None}

        for i in range(1, 6):
            response = self.session.request(method=method, url=url, params=params, 
                                            data=data, headers=headers, cookies=cookies,
                                            json=body, allow_redirects=allow_redirects, timeout=20)

            return response

        # 重试五次失败
        raise Exception("Request Error")
        
    def get(self, url: str, params: dict = None, headers: dict = None,
            cookies: dict = None, allow_redirects: bool = True) -> requests.Response:
        """..."""
        return self.request(method='GET', url=url, params=params, headers=headers,
                            cookies=cookies, allow_redirects=allow_redirects)

    def post(self, url: str, params: dict = None, headers: dict = None,
             data: dict = None, cookies: dict = None,
             body: dict = None, allow_redirects: bool = True) -> requests.Response:
        """..."""
        return self.request(method='POST', url=url, params=params,
                            data=data, headers=headers, cookies=cookies,
                            body=body, allow_redirects=allow_redirects)
