import time
from unittest import TestCase
import scene
import selene.logger


class TestScene(TestCase):
    def test_scene_state_change(self):
        a = scene.Scene(actions=None, config={"duration": 20})
        a.start()

        self.assertTrue(a.get_state())

        time.sleep(5)
        self.assertIn(a.get_time_elapsed(), [4, 5, 6])  # tolerances ~1s
        self.assertIn(a.get_time_remaining(), [14, 15, 16])  # tolerances ~1s

        a.stop()
        self.assertFalse(a.get_state())
