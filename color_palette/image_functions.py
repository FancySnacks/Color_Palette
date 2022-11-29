# Original code by Kyler Mintah
# https://www.kylermintah.me/
# Source: https://kylermintah.medium.com/coding-a-color-palette-generator-in-python-inspired-by-procreate-5x-b10df37834ae
# Edited for this program needs, I do not claim the ownership of this script


import math
import PIL
import extcolors
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from matplotlib import gridspec


def get_colors(img_path):
    img = PIL.Image.open(img_path)
    print(extract_colors(img))
    return extract_colors(img)

def colors_to_image(palette_colors: tuple, file):
    color_palette = render_color_palette(palette_colors, file)

def study_image(image_path):
    img = PIL.Image.open(image_path)
    colors = extract_colors(img)
    color_palette = render_color_palette(colors, None)
    overlay_palette(color_palette)

def extract_colors(img):
  tolerance = 32
  limit = 24
  colors, pixel_count = extcolors.extract_from_image(img, tolerance, limit)
  return colors

def render_color_palette(colors, file):
  size = 100
  columns = 6
  width = int(min(len(colors), columns) * size)
  height = int((math.floor(len(colors) / columns) + 1) * size)
  result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
  canvas = ImageDraw.Draw(result)
  for idx, color in enumerate(colors):
      x = int((idx % columns) * size)
      y = int(math.floor(idx / columns) * size)
      canvas.rectangle([(x, y), (x + size - 1, y + size - 1)], fill=color[0])
  result.save(file.name)
  return result

def overlay_palette(color_palette):
  nrow = 2
  ncol = 1
  f = plt.figure(figsize=(8,5), facecolor='None', edgecolor='k', dpi=55, num=None)
  gs = gridspec.GridSpec(nrow, ncol, wspace=0.0, hspace=0.0)
  f.add_subplot(2, 1, 1)
  plt.imshow(color_palette, interpolation='nearest')
  plt.axis('off')
  plt.subplots_adjust(wspace=0, hspace=0, bottom=0)
  plt.show(block=True)