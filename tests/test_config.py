from unittest import TestCase
import selene.config
import selene.logger
import confuse


class TestConfig(TestCase):
    def test_load_config(self):
        conf = selene.config.load()

        self.assertEqual(conf["deck_id"].get(int), 0)
        self.assertEqual(conf["font"].get(str), "roboto-regular")

    def test_config_missing_buttons(self):
        conf = confuse.Configuration('tests', __name__)
        conf.set_file('assets/config_missing_buttons.yaml')
        res = selene.config.check(conf, 5)

        self.assertFalse(res)

    def test_config_valid(self):
        conf = confuse.Configuration('tests', __name__)
        conf.set_file('assets/config_valid.yaml')
        res = selene.config.check(conf, 5)

        self.assertTrue(res)
