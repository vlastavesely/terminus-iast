#!/usr/bin/python3
# vim:set ts=4

import PIL
from bdf_font import BdfFont, Glyph
from os.path import basename
from PIL.Image import Image
from typing import List, Tuple

class Terminus:
	def __init__(self, files: List[str]) -> None:
		self.fonts = {file: BdfFont(file) for file in files}

	@classmethod
	def create(cls, src: str) -> 'Terminus':
		sizes = [12, 14, 16, 18, 20, 22, 24, 28, 32]
		files = [f'{src}/ter-u{s}{w}.bdf' for s in sizes for w in ('n', 'b')]
		return cls(files)

	def __getitem__(self, key: int) -> Image:
		glyphs = self.find_glyph(key)
		w, h = self.calculate_image_size(glyphs)
		image = PIL.Image.new(mode='L', size=(w, h), color='#aaa')
		x = 1
		for glyph in glyphs:
			bmp = glyph.to_bitmap()
			image.paste(bmp, (x, 1))
			x += glyph.bbW + 1
		return image

	def __setitem__(self, key: int, image: Image) -> None:
		x = 1
		for font in self.fonts.values():
			bmp = image.crop((x, 1, x + font.bbW, font.bbH + 1))
			glyph = font[key] if key in font else font.create_glyph(key)
			glyph.from_bitmap(bmp)
			x += font.bbW + 1

	def find_glyph(self, key: int) -> List[Glyph]:
		return [
			v for font in self.fonts.values() if isinstance(v := font[key], Glyph)
		]

	def calculate_image_size(self, glyphs: List[Glyph]) -> Tuple[int, int]:
		w = h = 0
		for glyph in glyphs:
			w += glyph.bbW + 1
			if h < glyph.bbH:
				h = glyph.bbH
		return w + 1, h + 2

	def save(self, dest_dir: str = '.') -> None:
		for file, font in self.fonts.items():
			font.save(f'{dest_dir}/{basename(file)}')
