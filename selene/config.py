import os
from logger import logger

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")
CACHE_PATH = "/tmp/selene"

CONFIG = {
    "deck_id": 0,
    "brightness": 30,
    "font": "roboto-regular",
    "keys": {
        0: {
            "icon": {
                "up": "sunrise",
                "down": "sunrise"
            },
            "label": "Sunrise",
            "duration": 30,
            "actions": {
                "hue.Hue": {
                    "light": "abcd",
                    "brightness": "30"
                },
            }
        },
        1: {
            "icon": {
                "up": "relax",
                "down": "relax"
            },
            "label": "Relax",
            "duration": 3600,
            "actions": {
                "sonos.Sonos": {
                    "share_link": "https://open.spotify.com/playlist/3yx7DjSural7eASDmd8Ah1",
                },
            }
        },
        2: {
            "icon": {
                "up": "sleep",
                "down": "sleep"
            },
            "label": "Sleep",
            "duration": 90,
            "actions": {
                "sonos.Sonos": {
                    "share_link": "https://open.spotify.com/playlist/7J2yJ5L2SBDyaTwmByhnxC",
                },
            }
        },
        3: {
            "icon": {
                "up": "empty",
                "down": "empty"
            },
            "duration": 0,
            "label": "",
            "actions": {}
        },
        4: {
            "icon": {
                "up": "empty",
                "down": "empty"
            },
            "label": "",
            "duration": 0,
            "actions": {}
        },
        5: {
            "icon": {
                "up": "empty",
                "down": "empty"
            },
            "label": "",
            "duration": 0,
            "actions": {}
        }
    },
    "actions": {
        "sonos.Sonos": {
            "ip": "192.168.1.229",
            "volume": 40,
            "status_light": True,
        },
        "hue.Hue": {
            "bridge_ip": "192.168.1"
        }
    },
}


def check_config(config: dict, deck_button_count: int) -> bool:
    keys = ["deck_id", "brightness", "font", "keys"]
    for key in keys:
        if key not in config.keys():
            logger.error("Please configure `{}`".format(key))
            return False

    if len(config["keys"]) != deck_button_count:
        logger.error("This deck has {} keys, please configure them all.".format(deck_button_count))
        return False

    for k, v in config["keys"].items():
        if "duration" not in v:
            logger.error("Please configure `duration` for key {}".format(k))
            return False
        if "icon" not in v:
            logger.error("Please configure `icon` for key {}".format(k))
            return False

    return True
