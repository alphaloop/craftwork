from utils import Minecraft
from mcpi import block

def makeTree(m, t, height):
    t = t.copy()
    for i in range(height):
        m.setBlock(t, block.WOOD)
        t.up(1)
    start = t.copy()
    start.backwards(3)
    start.left(3)
    end = start.copy()
    end.right(6)
    end.up(3)
    end.forwards(6)
    m.setBlocks(start,end,block.LEAVES)

def makeForest(m, t, height, length, width):
    for x in range(width):
        for y in range(length):
            makeTree(m, t, height)
            t.forwards(10)
        t.right(10)
        t.backwards(10*length)

def makePyramid(m, t, size, blockType):
    start = t.copy()
    end = start.copy().right(size).forwards(size)
    for i in range(round(size / 2)):
        m.setBlocks(start, end, blockType)
        start.up(1).right(1).forwards(1)
        end.up(1).left(1).backwards(1)





