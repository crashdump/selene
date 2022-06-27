import threading
import pluggy, plugins.specs
from logger import logger


class Action:
    def __init__(self, actions, config):
        self.t = threading.Timer
        self.state = False
        self.actions = []  # TODO: there can be multiple actions.
        self.config = config
        self.duration = config["duration"]

        self.plugin = pluggy.PluginManager("selene_v1")
        self.plugin.add_hookspecs(plugins.specs.Hooks)
        self.plugin.trace.root.setwriter(print)
        self.plugin.enable_tracing()

        for action in actions:
            self.plugin.register("plugins.actions.{}".format(action))

    def start(self):
        self.t = threading.Timer(self.duration, self.stop)
        self.t.start()

        self.plugin.hook.on(config=self.config)
        self.state = True

        logger.debug("Action started for {}s.".format(self.duration))

    def stop(self):
        self.plugin.hook.off(config=self.config)
        self.state = False
        self.t.cancel()
        logger.debug("Action stopped after {}s.".format(self.duration))

    def toggle(self):
        if self.state:
            self.stop()
        else:
            self.start()

    def get_name(self):
        return self.t.name

    def get_state(self):
        return self.state
