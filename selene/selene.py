#!/usr/bin/env python3

import os
import threading
import pluggy
from StreamDeck.DeviceManager import DeviceManager

from config import ASSETS_PATH, CONFIG, check_config
import timer
import render
from plugins.specs import PluginSpecs


class Selene:
    def __init__(self):
        self.stop_button_id = 0
        self.streamdecks = DeviceManager().enumerate()
        print("Found {} Stream Deck(s).\n".format(len(self.streamdecks)))

        self.plugins = pluggy.PluginManager("selene_v1")
        self.ct = timer.Timer(1)

    # Returns styling information for a key based on its name, position and state.
    def __get_key_style(self, button_id, button_config, state):
        font = "fonts/{}.ttf".format(CONFIG["font"])
        icon = "icons/{}.png".format(button_config["icon"]["down"])
        label = button_config["label"]
        if state:
            icon = "icons/{}.png".format(button_config["icon"]["up"])
            # label = countdown here

        if button_id == self.stop_button_id:
            label = "Stop"
            if self.ct.state:
                label = "{} s".format(self.ct.countdown)

        return {
            "name": button_id,
            "icon": os.path.join(ASSETS_PATH, icon),
            "font": os.path.join(ASSETS_PATH, font),
            "label": label
        }

    # Creates a new key image based on the key index, style and current key state
    # and updates the image on the StreamDeck.
    def __update_key_image(self, button_id, button_config, deck, state):
        # Determine what icon and label to use on the generated key.
        key_style = self.__get_key_style(button_id, button_config, state)

        # Generate the custom key with the requested image and label.
        image = render.key_image(deck, key_style["icon"], key_style["font"], key_style["label"])

        # Use a scoped-with on the deck to ensure we're the only thread using it right now.
        with deck:
            deck.set_key_image(button_id, image)

    def __update_stop_button_image(self, deck, state):
        self.__update_key_image(self.stop_button_id, CONFIG["stop_button"], deck, state)

    # Prints key state change information, updates rhe key image and performs any
    # associated actions when a key is pressed.
    def __key_change_callback(self, deck, key, state):
        print("Deck {} Key {} = {}".format(deck.id(), key, state), flush=True)

        # Update the key image based on the new key state.
        self.__update_key_image(key, CONFIG["buttons"][key], deck, state)

        # Do thing when a key is changing to the pressed state.
        if state:
            # echo = action_echo
            self.ct = timer.Timer(10)
            self.ct.set_tick_callback(self.__update_stop_button_image, (deck, state))
            self.ct.start()

            # Do the thing here.

    def load_plugins(self, plugins: list):
        self.plugins.add_hookspecs(PluginSpecs)
        for plugin in plugins:
            self.plugins.register(plugin)

        print(self.plugins.list_plugin_distinfo())
        print(self.plugins.list_name_plugin())

    def run(self):
        if len(self.streamdecks) < 1:
            print("No devices found.")
            exit(1)

        deck = self.streamdecks[CONFIG["deck_id"]]

        if not deck.is_visual():
            print("Only works with devices that have screens.")
            exit(1)

        deck.open()
        deck.reset()

        print("Opened '{}' device (serial number: '{}', fw: '{}')".format(
            deck.deck_type(), deck.get_serial_number(), deck.get_firmware_version()
        ))

        if not check_config(CONFIG, deck.key_count()):
            exit(1)

        deck.set_brightness(CONFIG["brightness"])

        for button_id, button_config in CONFIG["buttons"].items():
            self.__update_key_image(button_id, button_config, deck, False)

        self.stop_button_id = deck.key_count() - 1
        self.__update_key_image(self.stop_button_id, CONFIG["stop_button"], deck, False)  # Last button is the stop.

        # Register callback function for when a key state changes.
        deck.set_key_callback(self.__key_change_callback)

        # Wait until all deck handles are closed.
        for t in threading.enumerate():
            try:
                t.join()
            except RuntimeError:
                pass

    # Prints diagnostic information about a given StreamDeck.
    def info(self):
        for index, deck in enumerate(self.streamdecks):
            deck.open()
            deck.reset()

            image_format = deck.key_image_format()
            flip_description = {
                (False, False): "not mirrored",
                (True, False): "mirrored horizontally",
                (False, True): "mirrored vertically",
                (True, True): "mirrored horizontally/vertically",
            }
            print("Deck {} - {}.".format(index, deck.deck_type()))
            print("\t - ID: {}".format(deck.id()))
            print("\t - Serial: '{}'".format(deck.get_serial_number()))
            print("\t - Firmware Version: '{}'".format(deck.get_firmware_version()))
            print("\t - Key Count: {} (in a {}x{} grid)".format(
                deck.key_count(),
                deck.key_layout()[0],
                deck.key_layout()[1]))
            if deck.is_visual():
                print("\t - Key Images: {}x{} pixels, {} format, rotated {} degrees, {}".format(
                    image_format['size'][0],
                    image_format['size'][1],
                    image_format['format'],
                    image_format['rotation'],
                    flip_description[image_format['flip']]))
            else:
                print("\t - No Visual Output")

            deck.close()


if __name__ == '__main__':
    selene = Selene()
    selene.load_plugins(["plugins.echo.Echo()"])

    selene.info()
    selene.run()
