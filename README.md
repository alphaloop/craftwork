# Craftwork
Minecraft Python Library

Craftwork is a Python3 library that makes it easier to write code that does things in Minecraft. It uses the [mcpi](https://github.com/martinohanlon/mcpi) library under the covers, but provides a simpler interface and some useful tools to do cool stuff more easily.

## Setup
If you're new to programming Minecraft using Python, you'll need to setup a few things on your computer before you can start using this library.

### Raspberry Pi
If you have a Raspberry Pi with [Raspbian](https://www.raspbian.org/) installed, you should be able to get started with this library right away as Raspbian comes pre-installed with the Minecraft Pi edition of Minecraft, which is already set up for Python programming. [This guide](https://projects.raspberrypi.org/en/projects/getting-started-with-minecraft-pi) will help you get started programming Minecraft with `mcpi`. Once you're up and running, you can install and start using Craftwork to make things easier.

### PC, Mac and Linux
If you're running Minecraft on a PC, Mac or on a Linux machine, you'll need to install a few things before you can get started.

* Minecraft
* Spigot Server
* Raspberry Juice Spigot Extension

## Craftwork Modules
Craftwork contains the following modules:
* `craftwork.core` - contains core classes that make it easier to progream
* `craftwork.images` - contains classes for rendering images as blocks
* `craftwork.text` - contains classes for rendering text as blocks
* `craftwork.examples` - examples of how to use the library

## Usage

```
from craftwork import core

cw = core.Craftwork()
block = cw.get_player_block().forward(1)

```
