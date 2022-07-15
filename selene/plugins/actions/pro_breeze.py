import plugins
import logging


class Dehumidifier:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.plugin_name = "pro_breeze.Dehumidifier"
        self.ip = ""
        self.client = None

    def __load_config(self, config):
        config = config[self.plugin_name]
        self.logger.debug(config)

        if "ip" in config:
            self.ip = config["ip"]
        else:
            self.logger.error("No Dehumidifier IP configured.")

    def __get_client(self):
        return self.client

    @plugins.hookimpl
    def on(self, config):
        self.__load_config(config)
        client = self.__get_client()
        print(client)
        self.logger.info("Started dehumidifier on IP {}".format(self.ip))
        return True

    @plugins.hookimpl
    def off(self, config):
        self.__load_config(config)
        client = self.__get_client()
        print(client)
        self.logger.info("Stopped dehumidifier on IP {}".format(self.ip))
        return True

