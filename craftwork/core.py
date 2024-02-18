from mcpi.vec3 import Vec3
from mcpi.minecraft import Minecraft
from mcpi.block import Block as MCBlock
from dataclasses import dataclass

class Craftwork:

    def __init__(self):
        self._mc = Minecraft.create()
    
    def get_player_block(self):
        try:
            tile = self._mc.player.getTilePos()
            direction = self.get_player_direction()
        except:
            raise CraftworkError('Error getting player position/direction. Is there an active player?')
        return Block(self._mc, Position(tile.x, tile.y, tile.z), direction)

    def get_player_direction(self):
        return Direction(self._mc.player.getRotation())
    
    def get_block_at(self, x, y, z):
        try:
            direction = self.get_player_direction()
        except:
            # No active player, use north
            direction = Direction(0)
        return Block(self._mc, Position(x, y, z), direction)

    def set_blocks(self, bottomLeftFront, topRightBack, block_type):
        self._mc.setBlocks(bottomLeftFront.position._toVec3(), topRightBack.position._toVec3(), block_type)

    def copy_blocks(self, bottomLeftFrontBlock, width, height, depth):

        if not isinstance(bottomLeftFrontBlock, Block):
            raise CraftworkError('bottomLeftFrontBlock must be an instance of core.Block')

        b = bottomLeftFrontBlock.copy()
        blocks = []
        progress = 0
        total = (width+1) * (depth+1) * (height+1)
        for z in range(depth + 1):
            square = []
            for y in range(height + 1):
                line = []
                for x in range(width + 1):
                    block = b.get_block_type()
                    line.append(block)
                    progress = progress + 1
                    print("%d of %d" % (progress, total))
                    b.right(1)
                square.append(line)
                b.up(1)
                b.left(width + 1)
            blocks.append(square)
            b.forward(1)
            b.down(height + 1)

        return blocks
            
    def paste_blocks(self, bottomLeftFrontBlock, blocks):

        if not isinstance(bottomLeftFrontBlock, Block):
            raise CraftworkError('bottomLeftFrontBlock must be an instance of core.Block')

        b = bottomLeftFrontBlock.copy()
        for square in blocks:
            height = 0
            for line in square:
                width = 0
                for block in line:
                    b.set_block_type(block)
                    b.right(1)
                    width = width + 1
                b.up(1)
                b.left(width)
                height = height + 1
            b.forward(1)
            b.down(height)
        
class Position:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def _toVec3(self):
        return Vec3(self.x, self.y, self.z)
    
    def copy(self):
        return Position(self.x, self.y, self.z)

    def __eq__(self, rhs):
        if not isinstance(rhs, Position):
            return False
        return self.x == rhs.x and self.y == rhs.y and self.z == rhs.z
    
    def __str__(self):
        return '%d,%d,%d' % (self.x, self.y, self.z)

class Direction:
    def __init__(self, rotation):
        self._rotation = rotation

    def __eq__(self, rhs):
        if isinstance(rhs, Direction):
            return self._rotation == rhs._rotation
        else:
            return False
    
    def get_bearing(self):
        if self._rotation >= 315 or self._rotation < 45:
            return 'n'
        if self._rotation >= 45 and self._rotation < 135:
            return 'w'
        if self._rotation >=135 and self._rotation < 225:
            return 's'
        if self._rotation >=225 and self._rotation < 315:
            return 'e'

    def copy(self):
        return Direction(self._rotation)
    
    def __str__(self):
        return self.get_bearing()

class Block:
    def __init__(self, mc, position, direction):
        self._mc = mc
        if not isinstance(position, Position):
            raise CraftworkError('position must be an instance of Position')
        if not isinstance(direction, Direction):
            raise CraftworkError('direction must be an instance of Direction')
        self.position = position
        self.facing = direction

    def copy(self):
        return Block(self._mc, self.position.copy(), self.facing.copy())

    def right(self, distance):
        bearing = self.facing.get_bearing()
        if bearing == 'n':
            self.position.x = self.position.x - distance
        elif bearing == 's':
            self.position.x = self.position.x + distance
        elif bearing == 'w':
            self.position.z = self.position.z + distance
        elif bearing == 'e':
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
        bearing = self.facing.get_bearing()
        if bearing == 'n':
            self.position.z = self.position.z + distance
        elif bearing == 's':
            self.position.z = self.position.z - distance
        elif bearing == 'w':
            self.position.x = self.position.x + distance
        elif bearing == 'e':
            self.position.x = self.position.x - distance
        return self

    def back(self, distance):
        self.forward(-distance)
        return self

    def get_block_type(self):
        return self._mc.getBlock(self.position._toVec3())
    
    def set_block_type(self, block_type):
        self._mc.setBlock(self.position._toVec3(), block_type)

    def __str__(self):
        return '%s %s' % (self.position, self.facing)

# TODO Properly wrap block type

@dataclass
class CraftworkError(BaseException):
    message: str

BLOCKS = {
    "AIR"                 : MCBlock(0),
    "STONE"               : MCBlock(1),
    "GRASS"               : MCBlock(2),
    "DIRT"                : MCBlock(3),
    "COBBLESTONE"         : MCBlock(4),
    "WOOD_PLANKS"         : MCBlock(5),
    "SAPLING"             : MCBlock(6),
    "BEDROCK"             : MCBlock(7),
    "WATER_FLOWING"       : MCBlock(8),
    "WATER"               : MCBlock(8),
    "WATER_STATIONARY"    : MCBlock(9),
    "LAVA_FLOWING"        : MCBlock(10),
    "LAVA"                : MCBlock(10),
    "LAVA_STATIONARY"     : MCBlock(11),
    "SAND"                : MCBlock(12),
    "GRAVEL"              : MCBlock(13),
    "GOLD_ORE"            : MCBlock(14),
    "IRON_ORE"            : MCBlock(15),
    "COAL_ORE"            : MCBlock(16),
    "WOOD"                : MCBlock(17),
    "LEAVES"              : MCBlock(18),
    "GLASS"               : MCBlock(20),
    "LAPIS_LAZULI_ORE"    : MCBlock(21),
    "LAPIS_LAZULI_MCBlock": MCBlock(22),
    "SANDSTONE"           : MCBlock(24),
    "BED"                 : MCBlock(26),
    "RAIL_POWERED"        : MCBlock(27),
    "RAIL_DETECTOR"       : MCBlock(28),
    "COBWEB"              : MCBlock(30),
    "GRASS_TALL"          : MCBlock(31),
    "DEAD_BUSH"           : MCBlock(32),
    "WOOL"                : MCBlock(35),
    "FLOWER_YELLOW"       : MCBlock(37),
    "FLOWER_CYAN"         : MCBlock(38),
    "MUSHROOM_BROWN"      : MCBlock(39),
    "MUSHROOM_RED"        : MCBlock(40),
    "GOLD_MCBlock"        : MCBlock(41),
    "IRON_MCBlock"        : MCBlock(42),
    "STONE_SLAB_DOUBLE"   : MCBlock(43),
    "STONE_SLAB"          : MCBlock(44),
    "BRICK_MCBlock"       : MCBlock(45),
    "TNT"                 : MCBlock(46),
    "BOOKSHELF"           : MCBlock(47),
    "MOSS_STONE"          : MCBlock(48),
    "OBSIDIAN"            : MCBlock(49),
    "TORCH"               : MCBlock(50),
    "FIRE"                : MCBlock(51),
    "STAIRS_WOOD"         : MCBlock(53),
    "CHEST"               : MCBlock(54),
    "DIAMOND_ORE"         : MCBlock(56),
    "DIAMOND_MCBlock"     : MCBlock(57),
    "CRAFTING_TABLE"      : MCBlock(58),
    "FARMLAND"            : MCBlock(60),
    "FURNACE_INACTIVE"    : MCBlock(61),
    "FURNACE_ACTIVE"      : MCBlock(62),
    "SIGN_STANDING"       : MCBlock(63),
    "DOOR_WOOD"           : MCBlock(64),
    "LADDER"              : MCBlock(65),
    "RAIL"                : MCBlock(66),
    "STAIRS_COBBLESTONE"  : MCBlock(67),
    "SIGN_WALL"           : MCBlock(68),
    "DOOR_IRON"           : MCBlock(71),
    "REDSTONE_ORE"        : MCBlock(73),
    "TORCH_REDSTONE"      : MCBlock(76),
    "SNOW"                : MCBlock(78),
    "ICE"                 : MCBlock(79),
    "SNOW_MCBlock"        : MCBlock(80),
    "CACTUS"              : MCBlock(81),
    "CLAY"                : MCBlock(82),
    "SUGAR_CANE"          : MCBlock(83),
    "FENCE"               : MCBlock(85),
    "PUMPKIN"             : MCBlock(86),
    "NETHERRACK"          : MCBlock(87),
    "SOUL_SAND"           : MCBlock(88),
    "GLOWSTONE_MCBlock"   : MCBlock(89),
    "LIT_PUMPKIN"         : MCBlock(91),
    "STAINED_GLASS"       : MCBlock(95),
    "BEDROCK_INVISIBLE"   : MCBlock(95),
    "TRAPDOOR"            : MCBlock(96),
    "STONE_BRICK"         : MCBlock(98),
    "GLASS_PANE"          : MCBlock(102),
    "MELON"               : MCBlock(103),
    "FENCE_GATE"          : MCBlock(107),
    "STAIRS_BRICK"        : MCBlock(108),
    "STAIRS_STONE_BRICK"  : MCBlock(109),
    "MYCELIUM"            : MCBlock(110),
    "NETHER_BRICK"        : MCBlock(112),
    "FENCE_NETHER_BRICK"  : MCBlock(113),
    "STAIRS_NETHER_BRICK" : MCBlock(114),
    "END_STONE"           : MCBlock(121),
    "WOODEN_SLAB"         : MCBlock(126),
    "STAIRS_SANDSTONE"    : MCBlock(128),
    "EMERALD_ORE"         : MCBlock(129),
    "RAIL_ACTIVATOR"      : MCBlock(157),
    "LEAVES2"             : MCBlock(161),
    "TRAPDOOR_IRON"       : MCBlock(167),
    "FENCE_SPRUCE"        : MCBlock(188),
    "FENCE_BIRCH"         : MCBlock(189),
    "FENCE_JUNGLE"        : MCBlock(190),
    "FENCE_DARK_OAK"      : MCBlock(191),
    "FENCE_ACACIA"        : MCBlock(192),
    "DOOR_SPRUCE"         : MCBlock(193),
    "DOOR_BIRCH"          : MCBlock(194),
    "DOOR_JUNGLE"         : MCBlock(195),
    "DOOR_ACACIA"         : MCBlock(196),
    "DOOR_DARK_OAK"       : MCBlock(197),
    "GLOWING_OBSIDIAN"    : MCBlock(246),
    "NETHER_REACTOR_CORE" : MCBlock(247)
}