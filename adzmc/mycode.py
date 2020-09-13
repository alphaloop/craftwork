from mcpi import block
from time import sleep

def castFireBolt(m, distance):
    b = m.getPlayerTile().forward(1)
    for i in range(distance):
        m.setBlock(b, block.FIRE)
        sleep(0.05)
        b.forward(1)
    start = b.left(5).down(5)
    end = b.copy().right(10).up(10).forward(10)
    m.setBlocks(start, end, block.FIRE)

def castMagicFireSpell(m, width, length, height):
    start = m.getPlayerTile().left(width / 2)
    end = start.copy().right(width).forward(length).up(height)
    m.setBlocks(start, end, block.FIRE)
    
def makeTree(m, t, height):
    t = t.copy()
    for i in range(height):
        m.setBlock(t, block.WOOD)
        t.up(1)
    start = t.copy()
    start.back(3)
    start.left(3)
    end = start.copy()
    end.right(6)
    end.up(3)
    end.forward(6)
    m.setBlocks(start,end,block.LEAVES)

def makeForest(m, t, height, length, width):
    for x in range(width):
        for y in range(length):
            makeTree(m, t, height)
            t.forward(10)
        t.right(10)
        t.back(10*length)

def makePyramid(m, t, size, blockType):
    start = t.copy()
    end = start.copy().right(size).forward(size)
    for i in range(round(size / 2)):
        m.setBlocks(start, end, blockType)
        start.up(1).right(1).forward(1)
        end.up(1).left(1).back(1)

def makeSwimmingPool(m, t, length, width, depth):
    start = t.copy()
    end = start.copy().right(width).forward(length).down(depth)
    m.setBlocks(start, end, block.CLAY)
    start.right(1).forward(1)
    end.left(1).back(1).up(1)
    m.setBlocks(start, end, block.WATER)





