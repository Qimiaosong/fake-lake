import threading

from casdoor import CasdoorSDK
from fakelake.settings import global_settings

_settings = global_settings()


class AuthCasdoor:
    # 创建一个类属性，该线程锁用于在多线程环境下确保单例模式的正确实现
    _instance_lock = threading.Lock()

    def __init__(self) -> None:
        self._casdoor = CasdoorSDK(
            endpoint=_settings.user_center.endpoint,
            client_id=_settings.user_center.client_id,
            client_secret=_settings.user_center.client_secret,
            certificate=_settings.user_center.certificate,
            application_name=_settings.user_center.application_name,
            front_endpoint=_settings.user_center.front_endpoint
        )

    def __new__(cls):
        if not hasattr(AuthCasdoor, "_instance"):
            with AuthCasdoor._instance_lock:
                if not hasattr(AuthCasdoor, "_instance"):
                    AuthCasdoor._instance = object.__new__(cls)
        return AuthCasdoor._instance

    def get_auth_url(self):
        return self._casdoor.get_auth_link(_settings.user_center.callback_default_url)

    def get_user(self, code):
        access_token = self._casdoor.get_oauth_token(code=code)
        if access_token:
            decode_msg = self._casdoor.parse_jwt_token(access_token)
            return decode_msg
        return None




