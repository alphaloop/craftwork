from PIL import Image as PILImage
from mcpi import block

class Image:

  def __init__(self, width, height, data, blockMap):
      self.blockMap = blockMap
      self.width = width
      self.height = height
      self.data = data
      self.blockMap = blockMap

  def render(self, cw, startBlock, yInitFunction, yIncrementFunction):
    b = startBlock.copy()
    yInitFunction(b)
    for y in range(self.height):
      for x in range(self.width):
        b.set_block_type(self.blockMap[self.data[x + (y * self.width)]])
        b.right(1)
      b.left(self.width)
      yIncrementFunction(b)

  def render_flat(self, cw, topLeftBlock):
    self.render(cw, topLeftBlock, lambda b: None, lambda b: b.back(1))

  def render_tall(self, cw, bottomLeftBlock):
    self.render(cw, bottomLeftBlock, lambda b: b.up(self.height), lambda b: b.down(1))

class GreyscaleFileImage(Image):

  def __init__(self, filename):
    blockMap = { 
        0: block.Block(35, 15),
        1: block.Block(35, 7),
        2: block.Block(1),
        3: block.Block(35, 8),
        4: block.Block(35, 0)
    }
    image = self._convert_image_to_greyscale(PILImage.open(filename))
    data = list(image.getdata())
    super().__init__(image.size[0], image.size[1], data, blockMap)

  def _convert_image_to_greyscale(self, image):

    def snap_to_five_levels(p):
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

    return image.convert('L').point(snap_to_five_levels)