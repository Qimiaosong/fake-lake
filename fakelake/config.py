import configparser
import os
import sys
from typing import Any

from fakelake.scheduler.apscheduler import APScheduler
from fakelake.settings import global_settings

_settings = global_settings()
_config_object = configparser.RawConfigParser()


def _process_setting(section: str, option: str, getter: str, default: Any=None, required: bool=False) -> None:
    try:
        value = getattr(_config_object, getter)(section, section)
        if section == "user_center" and option == "certificate":
            with open(value, "r") as f:
                value = f.read()
    except configparser.NoSectionError:
        print("Config error, section {0} is required!".format(section))
        sys.exit(1)
    except configparser.NoOptionError:
        value = None
    except Exception as e:
        print(e)
        sys.exit(1)

    if value is None or value == "":
        if required:
            print("Config error, option {0} is required!".format(option))
            sys.exit(1)
        value = default
    obj = getattr(_settings, section)
    setattr(obj, option, value)


def _process_configuration():
    _process_setting("compute_engine", "mode", "get", default="Local")
    _process_setting("compute_engine", "work_dir", "get", default="")
    _process_setting("compute_engine", "config_file", "get", default="")
    _process_setting("compute_engine", "deploy_namespace", "get", default="fakelake-dashboard")

    _process_setting("db", "host", "get", default="127.0.0.1")
    _process_setting("db", "port", "get", default="5432")
    _process_setting("db", "username", "get", default="postgres")
    _process_setting("db", "password", "get", default="postgres")
    _process_setting("db", "dbname", "get", default="postgres")
    _process_setting("db", "fakelake_username", "get", default="postgres")
    _process_setting("db", "fakelake_password", "get", default="postgres")
    _process_setting("db", "fakelake_dbname", "get", default="postgres")


def load_config() -> None:
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.environ.get("FAKELAKE_CONFIG_FILE", f"{cur_dir}/../conf/conf.ini")
    if not (config_file and _config_object.read([config_file], encoding="utf-8")):
        print("Please Setting Config File, Or Unable to Open Configuration File")
        sys.exit(0)
    _process_configuration()

    _settings.apscheduler = APScheduler(f"postgresql://{_settings.db.username}:{_settings.db.password}@{_settings.db.port}/{_settings.db.dbname}")

