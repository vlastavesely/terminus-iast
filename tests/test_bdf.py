#!/usr/bin/python3
# vim:set ts=4

import unittest
from bdf_font.bdf_font import BdfFont
from bdf_font.glyph import Glyph
from pathlib import Path
from PIL.Image import Image

class TestBdfFont(unittest.TestCase):
	def load_test_font(self) -> BdfFont:
		font_path = Path(__file__).parent / 'fixtures' / 'font.bdf'
		return BdfFont(str(font_path))

	def test_bdf_font_load(self) -> None:
		font = self.load_test_font()
		self.assertTrue(isinstance(font, BdfFont))
		self.assertEqual(font.bbW, 6)
		self.assertEqual(font.bbH, 12)
		self.assertTrue(isinstance(font[55], Glyph))
		self.assertTrue(isinstance(font[97], Glyph))

	def test_glyph(self) -> None:
		font = self.load_test_font()
		image = font[97].to_bitmap()
		self.assertTrue(isinstance(image, Image))
		self.assertEqual(image.width, 6)
		self.assertEqual(image.height, 12)

	def test_glyph_bitmap(self) -> None:
		font = self.load_test_font()
		image = font[97].to_bitmap()
		glyph = font.create_glyph(11)
		glyph.from_bitmap(image)
		self.assertEqual(str(font[11]), str(font[97]))

if __name__ == '__main__':
	unittest.main()
