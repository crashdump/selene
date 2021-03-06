import time
from unittest import TestCase
import scene


class Config(TestCase):
    def test_check_timer(self):
        a = scene.Preset(actions=None, config={"duration": 20})
        a.start()

        assert a.get_state()

        time.sleep(5)
        assert a.get_time_elapsed() in [4, 5, 6]  # tolerances ~1s
        assert a.get_time_remaining() in [14, 15, 16]  # tolerances ~1s

        a.stop()
        assert not a.get_state()
