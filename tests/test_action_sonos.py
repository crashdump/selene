import time
from unittest import TestCase
import plugins.actions.sonos


class Sonos(TestCase):
    def test_on(self):
        sonos = plugins.actions.sonos.Sonos()
        result = sonos.on(config={
            'sonos.Sonos()': {
                'duration': 30,
                'ip': '192.168.1.229',
                'volume': 30,
                'status_light': True
            }
        })

        print(result)
        assert result["current_transport_status"] == "OK"
        assert result["current_transport_state"] in ["TRANSITIONING", "PLAYING"]

    def test_off(self):
        sonos = plugins.actions.sonos.Sonos()
        result = sonos.off(config={
            'sonos.Sonos()': {
                'duration': 30,
                'ip': '192.168.1.229',
                'volume': 30,
                'status_light': True
            }
        })

        print(result)
        assert result["current_transport_status"] == "OK"
        assert result["current_transport_state"] in ["TRANSITIONING", "STOPPED"]


