Selene
======

Control things in your house from a StreamDeck. 

![Selene](https://media.githubusercontent.com/media/crashdump/selene/main/docs/imgs/selene.jpeg)

This is mainly used to control the ambiance in my young daughter's room through a StreamDeck and a Raspberry PI. While
most of the actions, settings and icons are currently hardcoded, it may prove useful to someone else, hence I am
sharing it.

# Batteries Included

## Hue

Turn on (or off) lights; a timer can be specified to revert after a while.

You will need a user id on the Bridge, you can follow the steps [here](https://developers.meethue.com/develop/get-started-2/#so-lets-get-started) to get it. 

## Spotify

Starts a playlist; a timer can be specified to turn the music off after a while.

You will need to register your app at [My Dashboard](https://developer.spotify.com/dashboard/) to get the credentials
necessary to make authorized calls (a client id and client secret).

# Plugins

All actions, such as Hue or Spotify, are simple modules and writing your own should be easy.

# Prerequisites

## MacOS

`brew install hidapi`

You may need to set `DYLD_LIBRARY_PATH` to the relevant folder (e.g /opt/homebrew/lib) before running the program.

## Linux

`sudo apt install -y libjpeg-dev zlib1g-dev libopenjp2-7 libtiff5 libudev-dev libusb-1.0-0-dev libhidapi-libusb0 libjpeg9-dev`

`echo 'SUBSYSTEMS=="usb", ATTRS{idVendor}=="0fd9", GROUP="users", TAG+="uaccess"' | sudo tee /etc/udev/rules.d/10-streamdeck.rules
sudo udevadm control --reload-rules`

# How to run

1. Configure

Tweak and copy the example configuration file from `selene/config_default.yaml` to `$XDG_CONFIG_HOME/Selene/config.yaml`

2. Start

`poetry run`

3. Press a button and enjoy!