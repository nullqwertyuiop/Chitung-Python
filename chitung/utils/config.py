import json
import os
from pathlib import Path

from ..utils.models import Config, GroupConfigList

config_path = Path(Path(__file__).parent.parent) / "data" / "Config.json"
group_config_path = Path(Path(__file__).parent.parent) / "data" / "GroupConfig.json"

if not os.path.isdir(Path(Path(__file__).parent.parent) / "data"):
    os.mkdir(Path(Path(__file__).parent.parent) / "data")


def load_config() -> Config:
    if os.path.isfile(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = Config(**json.loads(f.read()))
    else:
        cfg = Config()
    return cfg


def save_config():
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(config.dict(), indent=4, ensure_ascii=False))


def reload_config():
    global config
    config = load_config()


def reset_config():
    global config
    config = Config()


config: Config = load_config()
save_config()


def load_group_config() -> GroupConfigList:
    if group_config_path.is_file():
        with group_config_path.open(mode="r", encoding="utf-8") as f:
            cfg_list = GroupConfigList(**json.loads(f.read()))
    else:
        cfg_list = GroupConfigList()
    return cfg_list


def save_group_config():
    with group_config_path.open(mode="w", encoding="utf-8") as f:
        f.write(json.dumps(group_config.dict(), indent=4, ensure_ascii=False))


def reload_group_config():
    global group_config
    group_config = load_config()


def reset_group_config():
    global group_config
    group_config = GroupConfigList()


group_config: GroupConfigList = load_group_config()
save_group_config()
