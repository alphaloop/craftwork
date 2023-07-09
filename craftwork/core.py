from mcpi.vec3 import Vec3
from mcpi.minecraft import Minecraft

class Craftwork:

    def __init__(self):
        self.mc = Minecraft.create()
    
    def get_player_block(self):
        tile = self.mc.player.getTilePos()
        return Block(self.mc, Position(tile.x, tile.y, tile.z), self.get_player_direction())

    def get_player_direction(self):
        return Direction(self.mc.player.getRotation())

    def copyBlocks(self, bottomLeftFrontBlock, width, height, depth):
        t = bottomLeftFrontBlock.copy()
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
            
    def pasteBlocks(self, bottomLeftFrontBlock, blocks):
        t = bottomLeftFrontBlock.copy()
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
        
class Position:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def toVec3(self):
        return Vec3(self.x, self.y, self.z)
    
    def copy(self):
        return Position(self.x, self.y, self.z)

    def __eq__(self, rhs):
        if not isinstance(rhs, Position):
            return False
        return self.x == rhs.x and self.y == rhs.y and self.z == rhs.z

class Direction:
    def __init__(self, rotation):
        if rotation >= 315 or rotation < 45:
            self.direction = 'n'
        if rotation >= 45 and rotation < 135:
            self.direction = 'w'
        if rotation >=135 and rotation < 225:
            self.direction = 's'
        if rotation >=225 and rotation < 315:
            self.direction = 'e'

    def __eq__(self, rhs):
        if isinstance(rhs, Direction):
            return self.direction == rhs.direction
        elif isinstance(rhs, str):
            return self.direction == rhs
        else:
            return False
        
    def copy(self):
        return Direction(self.direction)

class Block:
    def __init__(self, mc, position, direction):
        self.mc = mc
        if not isinstance(position, Position):
            raise 'position must be an instance of Position'
        if not isinstance(direction, Direction):
            raise 'direction must be an instance of Direction'
        self.position = position
        self.facing = direction

    def copy(self):
        return Block(self.mc, self.position.copy(), self.facing.copy())

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

    def getType(self):
        return self.mc.getBlock(self.position.toVec3())
    
    def setType(self, block_type):
        self.mc.setBlock(self.position.toVec3(), block_type)