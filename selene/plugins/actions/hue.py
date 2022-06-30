import plugins


class Hue:
    @plugins.hookimpl
    def on(self, config):
        return True

    @plugins.hookimpl
    def off(self, config):
        return True

