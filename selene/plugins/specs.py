import pluggy

hookspec = pluggy.HookspecMarker("selene_v1")


class PluginSpecs:
    """Specifications for the Pluggable Actions."""

    @hookspec
    def configure(self, config: list) -> bool:
        """Load the configuration and validate it.

        :param config: receiver of the plugin configuration
        :return: False if the configuration is missing or incorrect.
        """

    @hookspec
    def on(self):
        """Implements what happens when someone presses the button."""

    @hookspec
    def off(self):
        """Implements what happens when someone presses the button again, or when the timer reaches the end."""


