import pluggy

hookspec = pluggy.HookspecMarker("selene_v1")


class Hooks:
    """Specifications for the Pluggable Actions."""

    @hookspec
    def on(self, config):
        """Implements what happens when someone presses the button.

        :param config: receiver of the plugin configuration
        """

    @hookspec
    def off(self, config):
        """Implements what happens when someone presses the button again; or when the timer reaches the end.

        :param config: receiver of the plugin configuration
        """


