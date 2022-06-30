import plugins
from logger import logger


class Echo:
    def __init__(self):
        self.message = ""

    def __config(self, config) -> dict:
        if "message" in config:
            self.message = config["message"]
        else:
            logger.error("No message configured")

    @plugins.hookimpl
    def on(self, config):
        config = self.__config(config)
        logger.info("Echo on: {}".format(config["message"]))
        return

    @plugins.hookimpl
    def off(self, config):
        config = self.__config(config)
        logger.info("Echo off: {}".format(config["message"]))
        return
