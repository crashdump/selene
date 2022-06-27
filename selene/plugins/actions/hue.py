import plugins


class Hue:
    @plugins.hookimpl
    def on(self, config) -> bool:
        return True

    @plugins.hookimpl
    def off(self, config) -> bool:
        return True
