from mcpi.vec3 import Vec3
from mcpi.minecraft import Minecraft as MC
from mcpi import block
from PIL import Image

class Minecraft:

    def __init__(self, mc):
        self.mc = mc
    
    def getPlayerTile(self):
        return Tile(self.mc.player.getTilePos(), self.getCompass())

    def getCompass(self):
        x,y,z = self.mc.player.getTilePos()
        rotation = self.mc.player.getRotation()
        if rotation >= 315 or rotation < 45:
            return 'n'
        if rotation >= 45 and rotation < 135:
            return 'w'
        if rotation >=135 and rotation < 225:
            return 's'
        if rotation >=225 and rotation < 315:
            return 'e'

    def setBlock(self, tile, blockType):
        self.mc.setBlock(tile.toVec(), blockType)

    def getBlockType(self, tile):
        return self.mc.getBlock(tile.toVec())

    def setBlocks(self, fromTile, toTile, blockType):
        self.mc.setBlocks(fromTile.toVec(), toTile.toVec(), blockType)

    def copyBlocks(self, bottomLeftFrontTile, width, height, depth):
        t = bottomLeftFrontTile.copy()
        blocks = []
        progress = 0
        total = width * depth * height
        for z in range(depth + 1):
            square = []
            for y in range(height + 1):
                line = []
                for x in range(width + 1):
                    block = self.mc.getBlock(t.toVec())
                    line.append(block)
                    progress = progress + 1
                    print("%d of %d" % (progress, total))
                    t.right(1)
                square.append(line)
                t.up(1)
                t.left(width + 1)
            blocks.append(square)
            t.forward(1)
            t.down(height + 1)

        return blocks
            
    def pasteBlocks(self, bottomLeftFrontTile, blocks):
        t = bottomLeftFrontTile.copy()
        for square in blocks:
            height = 0
            for line in square:
                width = 0
                for block in line:
                    self.mc.setBlock(t.toVec(), block)
                    t.right(1)
                    width = width + 1
                t.up(1)
                t.left(width)
                height = height + 1
            t.forward(1)
            t.down(height)
        
    
class Tile:
    def __init__(self, position, facing):
        if not isinstance(position, Vec3):
            raise 'position must be a Vec3'
        if not facing in ['n','s','e','w']:
            raise 'invalid value for facing'
        self.position = position
        self.facing = facing

    def toVec(self):
        return self.position

    def copy(self):
        return Tile(self.position.clone(), self.facing)

    def __str__(self):
        (x,y,z) = self.toVec()
        return '(%d,%d,%d)' % (x,y,z)

    def right(self, distance):
        if self.facing == 'n':
            self.position.x = self.position.x - distance
        elif self.facing == 's':
            self.position.x = self.position.x + distance
        elif self.facing == 'w':
            self.position.z = self.position.z + distance
        elif self.facing == 'e':
            self.position.z = self.position.z - distance
        return self

    def left(self, distance):
        self.right(-distance)
        return self

    def up(self, distance):
        self.position.y = self.position.y + distance
        return self

    def down(self, distance):
        self.up(-distance)
        return self

    def forward(self, distance):
        if self.facing == 'n':
            self.position.z = self.position.z + distance
        elif self.facing == 's':
            self.position.z = self.position.z - distance
        elif self.facing == 'w':
            self.position.x = self.position.x + distance
        elif self.facing == 'e':
            self.position.x = self.position.x - distance
        return self

    def back(self, distance):
        self.forward(-distance)
        return self


class MCImage:

  def __init__(self, filename):
    self.colourBlockMap = { 
        0: block.Block(35, 15),
        1: block.Block(35, 7),
        2: block.Block(1),
        3: block.Block(35, 8),
        4: block.Block(35, 0)
    }
    image = self.convertImageTo4LevelGreyscale(Image.open(filename))
    self.width = image.size[0]
    self.height = image.size[1]
    self.data = self.convertImageToBlocks(image)

  def convertImageTo4LevelGreyscale(self, image):

    def snapTo5Levels(p):
      if p < 24:
        return 0
      elif p < 65:
        return 1
      elif p < 89:
        return 2
      elif p < 147:
        return 3
      else:
        return 4

    return image.convert('L').point(snapTo5Levels)

  def convertImageToBlocks(self, image):
    data = []
    for p in list(image.getdata()):
      data.append(self.colourBlockMap[p])
    return data

  def renderFlat(self, m, topLeftBlock):
    b = topLeftBlock.copy()
    for y in range(self.height):
      for x in range(self.width):
        m.setBlock(b, self.data[x + (y * self.width)])
        b.right(1)
      b.left(self.width)
      b.back(1)

  def renderTall(self, m, bottomLeftBlock):
    b = bottomLeftBlock.copy()
    b.up(self.height)
    for y in range(self.height):
      for x in range(self.width):
        m.setBlock(b, self.data[x + (y * self.width)])
        b.right(1)
      b.left(self.width)
      b.down(1)