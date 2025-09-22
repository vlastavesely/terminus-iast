#!/usr/bin/python3
# vim:set ts=4

from bdflib.model import Glyph as FontGlyph
from PIL import Image

class Glyph(FontGlyph):
	def to_bitmap(self) -> Image:
		w, h = self.bbW, self.bbH
		image = Image.new(mode='1', size=(w, h), color='#fff')
		buf = image.load()
		pixels = self.iter_pixels()
		for y in range(h):
			row = next(pixels)
			for x in range(w):
				buf[x, y] = 0 if next(row) else 1
		return image
