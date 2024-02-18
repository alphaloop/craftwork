# Craftwork
Minecraft Python Library

`craftwork` is a Python3 library that makes it easier to write code that does things in Minecraft. It uses the [mcpi](https://github.com/martinohanlon/mcpi) library under the covers, but provides a simpler interface and some useful tools to do stuff more easily.

The main difference between `craftwork` and `mcpi` is that `craftwork` allows you to talk about blocks relative to where the player is looking, making it easier to think about the blocks your code is working on without having to keep track of coordinates.

You don't have to have a player connected to use `craftwork`: if you don't you can still manipulate blocks, but `craftwork` will behave as if you are facing north, unless you tell it otherwise.

## SetupCraftwork
If you're new to programming Minecraft using Python, you'll need to setup a few things on your computer before you can start using this library.

### Raspberry Pi
If you have a Raspberry Pi with [Raspbian](https://www.raspbian.org/) installed, you should be able to get started with this library right away as Raspbian comes pre-installed with the Minecraft Pi edition of Minecraft, which is already set up for Python programming. [This guide](https://projects.raspberrypi.org/en/projects/getting-started-with-minecraft-pi) will help you get started programming Minecraft with `mcpi`. Once you're up and running, you can install and start using Craftwork to make things easier.

### PC, Mac and Linux
If you're running Minecraft on a PC, Mac or on a Linux machine, you'll need to install a few things before you can get started.

* Minecraft - You'll need Minecraft installed on a machine that can connect to the one you'll use to run the Minecraft server that your Python code will interact with. It doesn't have to be on the same machine as the one running the server, but it can be.
* Java - You'll need Java to run your Minecraft server. There are a few Java distributions available, which you may already have installed. If not you can download one [from the official Java site](https://www.java.com/en/download/help/download_options.html)
* Spigot Server - This is the Minecraft server your Python code will connect to to do stuff in Minecraft. You can install it using the [build tools](https://www.spigotmc.org/wiki/buildtools/).
* Raspberry Juice Minecraft Server Extension - This is an extension you can add to your Spigot Server that allows your Python code to talk to a server running on the same machine using `mcpi`. You can download the source code from [the github repository](https://github.com/zhuowei/RaspberryJuice) and build the extension using the instructions in the README file. This will build a `.jar` file in the `targets` directory that you'll need to copy into the `plugins` directory of your Spigot server install.

Once your Spigot server is up and running with the Raspberry Juice plugin installed, you should be able to run Python code using Craftwork on the same machine as the Spigot server.

Note: you will need to run a version of Spigot that matches the version of Minecraft you're using to connect to the server. Connect to your Spigot server the same way you'd connect to any Minecraft server. If Minecraft is running on the same machine as the Spigot server, enter the hostname `localhost` to connect.

## Craftwork Modules
Craftwork contains the following modules:
* `craftwork.core` - contains core classes that make it easier to progream
* `craftwork.images` - contains classes for rendering images as blocks
* `craftwork.text` - contains classes for rendering text as blocks
* `craftwork.examples` - examples of how to use the library

## Usage

The following code shows you how to get started with Craftwork:

```
# Import the craftware core module
from craftwork import core

# Create a new instance of Craftwork. This will connect to the Minecraft server running on the same machine
cw = core.Craftwork()

# Get the block the player is currently standing on. You will need to have an active player connected to the server for this to work
block = cw.get_player_block()

# You can change the block position that block refers to using the forward, backward, left, right, up and down methods
block.forward(1)
block.up(1)
# block now refers to the block position one block forward and one block up from the block the player is standing on
# these movements are relative to the direction the user was facing when get_player_block was called

# You can change the type of block
block.set_block_type(core.BLOCKS["STONE"])
# The block in front of the player is now a stone block

# You can chain these methods together for convinience
block = cw.get_player_block()
block.forward(10).up(1).left(1).set_block_type(core.BLOCKS["STONE"])
```
## Examples

Try some of the examples in the `examples` module to see what you can do with `craftwork`:

```
# Import the core and examples modules
from craftwork import core, examples

# Create a new instance of Craftwork.
cw = core.Craftwork()

# Select a block in front of the player
block = cw.get_player_block().forward(5)

# Plant a tree on that block
core.examples.make_tree(cw, block)
```