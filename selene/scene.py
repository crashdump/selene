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
        self.actions = []
        self.config = config

        self.plugin = pluggy.PluginManager("selene_v1")
        self.plugin.add_hookspecs(plugins.specs.Hooks)
        self.plugin.trace.root.setwriter(print)
        self.plugin.enable_tracing()

        if len(actions) == 0:
            logger.warning("No actions registered with key.")

        for action in actions:
            plugin = f"plugins.actions.{action}"
            print(plugin)
            self.plugin.register(eval(plugin)())

    def start(self):
        if self.timer_duration > 0:
            self.timer = threading.Timer(self.timer_duration, self.stop)
            self.timer.start()
            self.timer_start_time = datetime.now()
            self.plugin.hook.on(config=self.config["actions"])
            self.state = True
            logger.debug(f"Action started for {self.timer_duration}s.")
        logger.debug("We don't start the timer as duration configured to 0.")

    def stop(self):
        self.plugin.hook.off(config=self.config["actions"])
        self.state = False
        self.timer.cancel()
        logger.debug(f"Action stopped after {self.timer_duration}s.")

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
