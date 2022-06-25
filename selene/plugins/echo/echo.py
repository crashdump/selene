import plugins


class Echo:
    @plugins.hookimpl
    def __init__(self):
        self.config = None

    @plugins.hookimpl
    def configure(self, config):
        self.config = config
        return True if "message" in self.config else False

    @plugins.hookimpl
    def on(self):
        print("Echo on: {}".format(self.config["message"]))
        return

    @plugins.hookimpl
    def off(self):
        print("Echo off.")
        return
