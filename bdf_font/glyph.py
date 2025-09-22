#!/usr/bin/python3
# vim:set ts=4

import PIL
from bdflib.model import Glyph as FontGlyph
from functools import reduce
from PIL.Image import Image

class Glyph(FontGlyph): # type: ignore
	def to_bitmap(self) -> Image:
		w, h = self.bbW, self.bbH
		image = PIL.Image.new(mode='1', size=(w, h), color='#fff')
		buf = image.load()
		if not buf:
			raise RuntimeError('no pixels')
		pixels = self.iter_pixels()
		for y in range(h):
			row = next(pixels)
			for x in range(w):
				buf[x, y] = 0 if next(row) else 1
		return image

	def from_bitmap(self, image: Image, x: int = 0, y: int = 0) -> None:
		w, h = self.bbW, self.bbH
		pixels = image.load()
		if not pixels:
			raise RuntimeError('no pixels')
		data = []
		for i in range(h):
			bits = []
			for j in range(w):
				bits.append(1 if pixels[j + x, i + y] == 0 else 0)
			data.append(reduce(lambda acc, b: (acc << 1) | b, bits, 0))
		self.data = list(reversed(data))
