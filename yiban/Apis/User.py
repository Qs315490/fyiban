from yiban.Core import Login


class User:
    def __init__(self, mobile: str, password: str):
        self.__mobile = mobile
        self.__password = password
        self.__access_token = Login().get_user_access_token(self.__mobile, self.__password)

    def get_user_access_token(self) -> str:
        """获取用户登录密钥"""
        return self.__access_token

    # def get_user_name(self) -> str:
    #     """获取用户名"""
    #     return self.user['user']['name']

    # def get_user_phone(self) -> str:
    #     """获取用户手机号"""
    #     return self.user['user']['phone']

    # def get_user_school_name(self) -> str:
    #     """获取用户学校名称"""
    #     return self.user['user']['school']['schoolName']
