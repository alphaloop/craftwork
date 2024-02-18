from . import core
from time import sleep

def cast_fire_bolt(cw, distance):
    b = cw.get_player_block().forward(1)
    for i in range(distance):
        b.set_block_type(core.BLOCKS["FIRE"])
        sleep(0.05)
        b.set_block_type(core.BLOCKS["AIR"])
        b.forward(1)
    start = b.left(5)
    end = b.copy().right(10).up(10).forward(10)
    cw.set_blocks(start, end, core.BLOCKS["FIRE"])
    
def make_tree(cw, block, height):
    b = block.copy()
    for i in range(height):
        b.set_block_type(core.BLOCKS["WOOD"])
        b.up(1)
    start = b.copy()
    start.back(3)
    start.left(3)
    end = start.copy()
    end.right(6)
    end.up(3)
    end.forward(6)
    cw.set_blocks(start, end, core.BLOCKS["LEAVES"])

def make_forest(cw, block, height, length, width):
    for x in range(width):
        for y in range(length):
            make_tree(cw, block, height)
            block.forward(10)
        block.right(10)
        block.back(10*length)

def make_pyramid(cw, block, size, blockType):
    start = block.copy()
    end = start.copy().right(size).forward(size)
    for i in range(round(size / 2)):
        cw.set_blocks(start, end, blockType)
        start.up(1).right(1).forward(1)
        end.up(1).left(1).back(1)

def make_swimming_pool(cw, block, length, width, depth):
    start = block.copy()
    end = start.copy().right(width).forward(length).down(depth)
    cw.set_blocks(start, end, core.BLOCKS["CLAY"])
    start.right(1).forward(1)
    end.left(1).back(1).up(1)
    cw.set_blocks(start, end, core.BLOCKS["WATER"])
