import plugins
import asyncio
from hue import Bridge, Light


class Hue:
    @staticmethod
    def __toggle_lights(config, state) -> list:
        out = []
        config = config["hue.Hue"]

        for light_config in config["lights"]:
            light = Light(light_config["id"], ip=config["ip"], user=config["secret"])
            light_info = asyncio.run(light.get_info())
            print(light_info)
            if "error" in light_info.keys():
                return light_info

            if state:
                out.append(asyncio.run(light.power_on()))
            else:
                out.append(asyncio.run(light.power_off()))

        return out

    @plugins.hookimpl
    def on(self, config):
        return self.__toggle_lights(config, True)

    @plugins.hookimpl
    def off(self, config):
        return self.__toggle_lights(config, False)

