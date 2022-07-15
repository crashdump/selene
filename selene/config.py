import os
import confuse
from logger import logger


class Config:
    def __init__(self):
        self.path_assets = os.path.join(os.path.dirname(__file__), "assets")
        self.path_cache = "/tmp/selene"
        self.deck_id = 0
        self.brightness = 30
        self.__font = ""
        self.__keys = {}
        self.__actions = []
        self.__default_config = {
            "actions": {},
            "duration": 3600,
            "label": "",
            "icon": "empty",
        }

    def load(self):
        config = confuse.Configuration('Selene', __name__)
        try:
            if "config.selene.cdfr.net/v1" != config["api"].get(str):
                logger.error("configuration api unknown")
                exit(1)
            self.__keys = config["keys"].get(list)
            self.__actions = config["actions"].get(dict)
            self.__font = config["font"].get(str)
            self.deck_id = config["deck_id"].get(int)
            self.brightness = config["brightness"].get(int)
        except confuse.exceptions.NotFoundError:
            logger.error("configuration file likely missing")
            exit(1)

    def get_keys(self) -> dict:
        return self.__keys

    def get_key(self, key: int) -> dict:
        try:
            key_config = self.__keys[key]
            for action in key_config["actions"].keys():
                key_config["actions"][action] = key_config["actions"][action] | self.__actions[action]
            return key_config
        except IndexError:
            return self.__default_config

    def get_key_actions(self, key: int) -> dict:
        try:
            return self.__keys[key]["actions"].keys()
        except IndexError:
            return {}

    def get_key_duration(self, key: int) -> int:
        try:
            return self.__keys[key]["duration"]
        except IndexError:
            return 3600

    def get_key_label(self, key: int) -> str:
        return self.__keys[key]["label"]

    def get_key_icon_path(self, key_id: int) -> str:
        return f"{self.path_assets}/icons/{self.get_key(key_id)['icon']}.png"

    def get_font_path(self) -> str:
        return f"{self.path_assets}/fonts/{self.__font}.ttf"

    def is_valid(self) -> bool:
        if self.__font == "":
            logger.error("Font not configured")
            return False

        if len(self.__keys) == 0:
            logger.error("Keys not configured")
            return False

        for key in self.__keys:
            if "duration" not in key:
                logger.error(f"Please configure `duration` for key {key}")
                return False
            if "icon" not in key:
                logger.error(f"Please configure `icon` for key {key}")
                return False

        return True
