import os

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

CONFIG = {
    "deck_id": 0,
    "brightness": 30,
    "font": "roboto-regular",
    "buttons": {
        0: {
            "icon": {
                "up": "sunrise",
                "down": "sunrise"
            },
            "label": "Sunrise",
            "actions": {
                "spotify": {
                    "state": "on",
                    "timer": 30,
                    "config": {
                        "song": "abcd",
                    }
                },
                "hue": {
                    "state": "on",
                    "timer": 30,
                    "config": {
                        "light": "abcd",
                        "brightness": "30"
                    }
                },
                "echo": {
                    "state": "on",
                    "timer": 30,
                    "config": {
                        "message": "Hello World!"
                    }
                }
            }
        },
        1: {
            "icon": {
                "up": "relax",
                "down": "relax"
            },
            "label": "Relax",
            "actions": {}
        },
        2: {
            "icon": {
                "up": "sleep",
                "down": "sleep"
            },
            "label": "Sleep",
            "actions": {}
        },
        3: {
            "icon": {
                "up": "empty",
                "down": "empty"
            },
            "label": "",
            "actions": {}
        },
        4: {
            "icon": {
                "up": "empty",
                "down": "empty"
            },
            "label": "",
            "actions": {}
        }
    },
    "stop_button": {
        "icon": {
            "up": "stop",
            "down": "stop"
        },
        "label": "Stop",
        "actions": {
            "spotify": {
                "state": "off"
            },
            "hue": {
                "state": "off"
            },
        }
    }
}


def check_config(config: dict, deck_button_count: int) -> bool:
    keys = ["deck_id", "brightness", "font", "buttons"]
    for k in keys:
        if not k in config.keys():
            print("Please configure `{}`".format(k))
            return False

    c = deck_button_count - 1  # Last one is for the stop button
    for i in range(0, c):
        if not config["buttons"][i]:
            print("Please configure all {} buttons".format(c))
            return False

        if "icon" not in config["buttons"][i]:
            print("Please configure `icon` for button {}".format(c))
            return False

    return True
