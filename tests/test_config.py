from unittest import TestCase
import selene.config as config


class Config(TestCase):
    def test_check_config(self):
        # empty config should return False
        res = config.check_config({}, 5)
        self.assertFalse(res)

        # missing button should return False
        res = config.check_config({
            "deck_id": 0,
            "brightness": 0,
            "font": "roboto-regular",
            "buttons": [
                {
                    "id": 0,
                    "icon": {
                        "up": "sunrise",
                        "down": "sunrise"
                    },
                    "label": "Sunrise",
                    "actions": {}
                },
                # button `1` is missing.
                {
                    "id": 2,
                    "icon": {
                        "up": "sleep",
                        "down": "sleep"
                    },
                    "label": "Sleep",
                    "actions": {}
                },
                {
                    "id": 3,
                    "icon": {
                        "up": "empty",
                        "down": "empty"
                    },
                    "label": "",
                    "actions": {}
                },
                {
                    "id": 4,
                    "icon": {
                        "up": "empty",
                        "down": "empty"
                    },
                    "label": "",
                    "actions": {}
                }
            ],
            "stop_button": {
                "icon": {
                    "up": "stop",
                    "down": "stop"
                },
                "label": "Stop",
                "actions": {},
            }
        }, 5)
        self.assertFalse(res)

        # valid config should return True
        res = config.check_config({
            "deck_id": 0,
            "brightness": 30,
            "font": "roboto-regular",
            "buttons": [
                {
                    "id": 0,
                    "icon": {
                        "up": "sunrise",
                        "down": "sunrise"
                    },
                    "label": "Sunrise",
                    "actions": {}
                },
                {
                    "id": 1,
                    "icon": {
                        "up": "relax",
                        "down": "relax"
                    },
                    "label": "Relax",
                    "actions": {}
                },
                {
                    "id": 2,
                    "icon": {
                        "up": "sleep",
                        "down": "sleep"
                    },
                    "label": "Sleep",
                    "actions": {}
                },
                {
                    "id": 3,
                    "icon": {
                        "up": "empty",
                        "down": "empty"
                    },
                    "label": "",
                    "actions": {}
                },
                {
                    "id": 4,
                    "icon": {
                        "up": "empty",
                        "down": "empty"
                    },
                    "label": "",
                    "actions": {}
                }
            ],
            "stop_button": {
                "icon": {
                    "up": "stop",
                    "down": "stop"
                },
                "label": "Stop",
                "actions": {},
            }
        }, 5)
        self.assertTrue(res)
