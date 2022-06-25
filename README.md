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

## Spotify

Starts a playlist; a timer can be specified to turn the music off after a while.

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

`poetry run`