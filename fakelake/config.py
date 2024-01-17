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