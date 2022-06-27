import plugins
import logging
from soco import SoCo
from soco.plugins.sharelink import ShareLinkPlugin


class Sonos:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ip = ""
        self.status_light = True
        self.volume = 20
        self.share_link = "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT?si=7209bd113488449a"

    def __config(self, config):
        if "share_link" in config:
            self.share_link = config["share_link"]
        else:
            self.logger.error("No music share link configured.")

        if "ip" in config:
            self.ip = config["ip"]
        else:
            self.logger.error("No Sonos IP configured.")

        if "volume" in config:
            self.volume = config["volume"]

        if "status_light" in config:
            self.status_light = config["status_light"]

    def __get_soco(self) -> SoCo:
        speaker = SoCo(self.ip)
        speaker.status_light = self.status_light
        speaker.volume = self.volume
        return speaker

    @plugins.hookimpl
    def on(self, config):
        self.logger.debug(config)
        self.__config(config)

        speaker = self.__get_soco()
        speaker.clear_queue()
        slp = ShareLinkPlugin(speaker)
        slp.add_share_link_to_queue(self.share_link)
        speaker.play()

        self.logger.info("Playing {} on {}".format(self.share_link, self.ip))
        self.logger.info(speaker.speaker_info)

    @plugins.hookimpl
    def off(self, config):
        self.__config(config)
        speaker = self.__get_soco()
        speaker.stop()

        self.logger.info("Stopped music on {}".format(self.ip))

