#!/usr/bin/env python3

# External
import os
import asyncio
import threading
from StreamDeck.DeviceManager import DeviceManager

# Internal
from config import ASSETS_PATH, CONFIG, check_config
from logger import logger
import action
import render

# Plugins
from plugins.specs import Hooks
import plugins.actions


class Selene:
    def __init__(self):
        self.stop_button_id = 0
        self.streamdecks = DeviceManager().enumerate()
        logger.info("Found {} Stream Deck(s).\n".format(len(self.streamdecks)))

        self.keys = {}

    def __update_all_keys(self, loop, deck):
        for button_id, button_config in CONFIG["keys"].items():
            self.__update_key_image(button_id, button_config, deck, False)

        loop.call_later(1, self.__update_all_keys, (loop, deck))

    # Returns styling information for a key based on its name, position and state.
    def __get_key_style(self, button_id, button_config, state):
        font = "fonts/{}.ttf".format(CONFIG["font"])
        icon = "icons/{}.png".format(button_config["icon"]["down"])
        label = button_config["label"]
        if state:
            icon = "icons/{}.png".format(button_config["icon"]["up"])

        # if button_id == self.stop_button_id:
        #     if self.ticker_stop.state and self.ticker_stop.countdown > 0:
        #         label = "{} s".format(self.ticker_stop.countdown)

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

    # Prints key state change information, updates rhe key image and performs any
    # associated actions when a key is pressed.
    def __key_change_callback(self, deck, key, state):
        logger.info("Deck {} Key {} = {}".format(deck.id(), key, state))

        # Update the key image based on the new key state.
        self.__update_key_image(key, CONFIG["keys"][key], deck, state)

        # Do thing when a key is changing to the pressed state.
        if state:
            self.keys[key].toggle()

    def run(self):
        if len(self.streamdecks) < 1:
            logger.error("No devices found.")
            exit(1)

        deck = self.streamdecks[CONFIG["deck_id"]]

        if not deck.is_visual():
            logger.error("Only works with devices that have screens.")
            exit(1)

        deck.open()
        deck.reset()
        deck.set_brightness(CONFIG["brightness"])

        logger.info("Opened '{}' device (serial number: '{}', fw: '{}')".format(
            deck.deck_type(), deck.get_serial_number(), deck.get_firmware_version()
        ))

        if not check_config(CONFIG, deck.key_count()):
            exit(1)

        # Event loop to update the keys every second.
        loop = asyncio.get_event_loop()
        self.__update_all_keys(loop, deck)

        for key in range(0, deck.key_count() ):
            print("Loading config for key {}".format(key))
            config = {}
            if "actions" in CONFIG["keys"][key]:
                config = CONFIG["keys"][key]["actions"] | CONFIG["actions"]
                config["duration"] = CONFIG["keys"][key]["duration"]
                config["label"] = CONFIG["keys"][key]["label"]
                print(config)

            self.keys[key] = self.keys[key] = action.Action(CONFIG["keys"][key]["actions"], config)

        # Key press callback
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
            logger.info("Deck {} - {}.".format(index, deck.deck_type()))
            logger.info("\t - ID: {}".format(deck.id()))
            logger.info("\t - Serial: '{}'".format(deck.get_serial_number()))
            logger.info("\t - Firmware Version: '{}'".format(deck.get_firmware_version()))
            logger.info("\t - Key Count: {} (in a {}x{} grid)".format(
                deck.key_count(),
                deck.key_layout()[0],
                deck.key_layout()[1]))
            if deck.is_visual():
                logger.info("\t - Key Images: {}x{} pixels, {} format, rotated {} degrees, {}".format(
                    image_format['size'][0],
                    image_format['size'][1],
                    image_format['format'],
                    image_format['rotation'],
                    flip_description[image_format['flip']]))
            else:
                logger.error("\t - No Visual Output")

            deck.close()


if __name__ == '__main__':
    selene = Selene()
    selene.info()
    selene.run()
