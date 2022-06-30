import threading
import pluggy
import plugins.specs
from datetime import datetime, timedelta
from logger import logger


class Scene:
    def __init__(self, actions, config):
        self.timer = threading.Timer
        self.timer_duration = config["duration"]
        self.timer_start_time = None

        self.state = False
        self.actions = []  # TODO: there can be multiple actions.
        self.config = config

        self.plugin = pluggy.PluginManager("selene_v1")
        self.plugin.add_hookspecs(plugins.specs.Hooks)
        self.plugin.trace.root.setwriter(print)
        self.plugin.enable_tracing()

        if len(actions) == 0:
            logger.warning("No actions registered with key.")

        for action in actions:
            plugin = "plugins.actions.{}".format(action)
            print(plugin)
            self.plugin.register(eval(plugin)())

    def start(self):
        self.timer = threading.Timer(self.timer_duration, self.stop)
        self.timer.start()
        self.timer_start_time = datetime.now()
        self.plugin.hook.on(config=self.config)
        self.state = True
        logger.debug("Action started for {}s.".format(self.timer_duration))

    def stop(self):
        self.plugin.hook.off(config=self.config)
        self.state = False
        self.timer.cancel()
        logger.debug("Action stopped after {}s.".format(self.timer_duration))

    def toggle(self):
        if self.state:
            self.stop()
        else:
            self.start()

    def get_name(self) -> str:
        return self.timer.name

    def get_state(self) -> bool:
        return self.state

    def get_time_elapsed(self) -> int:
        return (datetime.now() - self.timer_start_time).seconds

    def get_time_remaining(self) -> int:
        end = self.timer_start_time + timedelta(seconds=self.timer_duration)
        return (end - datetime.now()).seconds
