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


class Settings:
    compute_engine = ComputeEngine()
    db = DB()


_settings = Settings()


def global_settings():
    return _settings

