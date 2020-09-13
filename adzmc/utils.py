from mcpi.vec3 import Vec3
from mcpi.minecraft import Minecraft as MC
from mcpi import block

class Minecraft:

    def __init__(this, mc):
        this.mc = mc
    
    def getPlayerTile(this):
        return Tile(this.mc.player.getTilePos(), this.getCompass())

    def getCompass(this):
        x,y,z = this.mc.player.getTilePos()
        rotation = this.mc.player.getRotation()
        if rotation >= 315 or rotation < 45:
            return 'n'
        if rotation >= 45 and rotation < 135:
            return 'w'
        if rotation >=135 and rotation < 225:
            return 's'
        if rotation >=225 and rotation < 315:
            return 'e'
        
    def setBlock(this, tile, blockType):
        this.mc.setBlock(tile.toVec(), blockType)

    def setBlocks(this, fromTile, toTile, blockType):
        this.mc.setBlocks(fromTile.toVec(), toTile.toVec(), blockType)

    def copyBlocks(this, bottomLeftFrontTile, width, height, depth):
        t = bottomLeftFrontTile.copy()
        blocks = []
        progress = 0
        total = width * depth * height
        for z in range(depth + 1):
            square = []
            for y in range(height + 1):
                line = []
                for x in range(width + 1):
                    block = this.mc.getBlock(t.toVec())
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
            
    def pasteBlocks(this, bottomLeftFrontTile, blocks):
        t = bottomLeftFrontTile.copy()
        for square in blocks:
            height = 0
            for line in square:
                width = 0
                for block in line:
                    this.mc.setBlock(t.toVec(), block)
                    t.right(1)
                    width = width + 1
                t.up(1)
                t.left(width)
                height = height + 1
            t.forward(1)
            t.down(height)
        
    
class Tile:
    def __init__(this, position, facing):
        if not isinstance(position, Vec3):
            raise 'position must be a Vec3'
        if not facing in ['n','s','e','w']:
            raise 'invalid value for facing'
        this.position = position
        this.facing = facing

    def toVec(this):
        return this.position

    def copy(this):
        return Tile(this.position.clone(), this.facing)

    def __str__(this):
        (x,y,z) = this.toVec()
        return '(%d,%d,%d)' % (x,y,z)

    def right(this, distance):
        if this.facing == 'n':
            this.position.x = this.position.x - distance
        elif this.facing == 's':
            this.position.x = this.position.x + distance
        elif this.facing == 'w':
            this.position.z = this.position.z + distance
        elif this.facing == 'e':
            this.position.z = this.position.z - distance
        return this

    def left(this, distance):
        this.right(-distance)
        return this

    def up(this, distance):
        this.position.y = this.position.y + distance
        return this

    def down(this, distance):
        this.up(-distance)
        return this

    def forward(this, distance):
        if this.facing == 'n':
            this.position.z = this.position.z + distance
        elif this.facing == 's':
            this.position.z = this.position.z - distance
        elif this.facing == 'w':
            this.position.x = this.position.x + distance
        elif this.facing == 'e':
            this.position.x = this.position.x - distance
        return this

    def back(this, distance):
        this.forward(-distance)
        return this

    
        
