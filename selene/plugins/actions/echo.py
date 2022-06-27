import plugins
from logger import logger

class Echo:
    @plugins.hookimpl
    def on(self, config):
        logger.info("Echo on: {}".format(config["message"]))
        return

    @plugins.hookimpl
    def off(self, config):
        logger.info("Echo off: {}".format(config["message"]))
        return
