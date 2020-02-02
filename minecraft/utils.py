from mcpi.vec3 import Vec3
from mcpi.minecraft import Minecraft as MC
from mcpi import block

class Minecraft:

    def __init__(this):
        this.mc = MC.create()
    
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
        if fromTile.facing in ['n','s']:
            this.mc.setBlocks(toTile.toVec(), fromTile.toVec(), blockType)
        else:
            this.mc.setBlocks(fromTile.toVec(), toTile.toVec(), blockType)
    
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
        if this.facing in ['n','s']:
            this.position.x = this.position.x + distance
        else:
            this.position.z = this.position.z + distance
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

    def forwards(this, distance):
        if this.facing in ['n','s']:
            this.position.z = this.position.z + distance
        else:
            this.position.x = this.position.x + distance
        return this

    def backwards(this, distance):
        this.forwards(-distance)
        return this

    
        
