from typing import Any, Iterator, Tuple


class ComputeEngine:
    mode: str
    work_dir: str
    config_file: str = None
    deployment_namespace: str = None


class DB:
    host: str
    port: int
    username: str
    password: str
    dbname: str
    fakelake_username: str
    fakelake_password: str
    fakelake_dbname: str


class CurrentUser:
    user_name: str
    pg_password: str
    workspace_name: str


class UserCenter:
    endpoint: str
    front_endpoint: str
    client_id: str
    client_secret: str
    certificate: str
    org_name: str
    application_name: str
    callback_default_url: str


class ProductInfo:
    product_name: str
    product_type: int
    datasource_count: int
    workspace_count: int
    user_count: int
    support_jdbc_query: str
    tech_support: str


class Settings:
    compute_engine = ComputeEngine()
    db = DB()
    current_user = CurrentUser()
    product_info = ProductInfo()
    user_center = UserCenter()


_settings = Settings()


def global_settings():
    return _settings

