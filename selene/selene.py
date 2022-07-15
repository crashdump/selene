#!/usr/bin/env python3

import asyncio
import sys

from StreamDeck.DeviceManager import DeviceManager

from logger import logger
from scene import Scene
from config import Config
import render

from plugins.specs import Hooks
import plugins.actions


class Selene:
    def __init__(self):
        self.streamdecks = DeviceManager().enumerate()
        logger.info(f"Found {len(self.streamdecks)} Stream Deck(s).\n")

        self.display_refresh = .5  # seconds
        self.scenes = {}
        self.scene_active = False
        self.config = Config()

    async def __update_keys(self, deck):
        while True:
            await asyncio.sleep(self.display_refresh)
            for i in range(0, len(self.config.get_keys())):
                self.__update_key_image(i, deck)

    # Prints key state change information, updates rhe key image and performs any
    # associated actions when a key is pressed.
    def __on_key_change(self, deck, key, pressed):
        logger.info(f"Deck {deck.id()} Key {key} = {pressed}")

        # Update the key image based on the new key state.
        self.__update_key_image(key, deck)

        if pressed:  # Do thing when a key is changing to the pressed state.
            self.scenes[key].toggle()

    # Creates a new key image based on the key index, style and current key state
    # and updates the image on the StreamDeck.
    def __update_key_image(self, key_id, deck):
        # Determine what label to use on the generated key.
        label = self.config.get_key_label(key_id)
        if self.scenes[key_id].get_state():
            minutes, seconds = divmod(self.scenes[key_id].get_time_remaining(), 60)
            label = f"{minutes}s"
            if minutes > 0:
                label = f"{minutes}m{seconds}s"

        # Use a scoped-with on the deck to ensure we're the only thread using it right now.
        image = render.key_image(deck, self.config.get_key_icon_path(key_id), self.config.get_font_path(), label)
        with deck:
            deck.set_key_image(key_id, image)

    def run(self):
        if len(self.streamdecks) < 1:
            logger.error("No devices found.")
            sys.exit(1)

        self.config = Config()
        self.config.load()
        if not self.config.is_valid():
            sys.exit(1)

        deck = self.streamdecks[self.config.deck_id]

        if not deck.is_visual():
            logger.error("Only works with devices that have screens.")
            sys.exit(1)

        deck.open()
        deck.reset()
        deck.set_brightness(self.config.brightness)

        logger.info(f"Opened '{deck.deck_type()}' device (serial number: '{deck.get_serial_number()}',"
                    f"fw: '{deck.get_firmware_version()}')")

        # Init the "Action" objects for each key: self.keys[n]
        for key in range(0, deck.key_count()):
            logger.debug(f"Loading config for key {key}")
            self.scenes[key] = Scene(self.config.get_key_actions(key), self.config.get_key(key))

        # Key press callback
        deck.set_key_callback(self.__on_key_change)

        # Event loop to update the keys every second.
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__update_keys(deck))
        loop.run_forever()

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
            logger.info(f"Deck {index} - {deck.deck_type()}.")
            logger.info(f"\t - ID: {deck.id()}")
            logger.info(f"\t - Serial: '{deck.get_serial_number()}'")
            logger.info(f"\t - Firmware Version: '{deck.get_firmware_version()}'")
            logger.info(f"\t - Key Count: {deck.key_count()} (in a {deck.key_layout()[0]}x{deck.key_layout()[1]} grid)")
            if deck.is_visual():
                logger.info(f"\t - Key Images: {image_format['size'][0]}x{image_format['size'][1]} pixels, "
                            f"{image_format['format']} format, rotated {image_format['rotation']} degrees, "
                            f"{flip_description[image_format['flip']]}")
            else:
                logger.error("\t - No Visual Output")

            deck.close()


if __name__ == '__main__':
    selene = Selene()
    selene.info()
    selene.run()
