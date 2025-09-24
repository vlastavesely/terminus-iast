#!/usr/bin/python3
# vim:set ts=4

from bdf_font.glyph import Glyph
from bdflib.model import Font
from bdflib import reader, writer
from typing import Union

PropertyValue = Union[bytes, int]

class BdfFont(Font): # type: ignore
	def __new__(cls, file_name: str): # type: ignore
		with open(file_name, 'rb') as f:
			font = reader.read_bdf(f)
		font.__class__ = cls
		return font

	def __init__(self, file_name: str) -> None:
		# already initialised by the reader factory
		pass

	def __getitem__(self, key: int) -> Glyph:
		ret = self.glyphs_by_codepoint[key]
		ret.__class__ = Glyph
		return ret # type: ignore

	@property
	def bbW(self) -> int:
		return int(self.get_reference_char().bbW)

	@property
	def bbH(self) -> int:
		return int(self.get_reference_char().bbH)

	def get_reference_char(self) -> Glyph:
		glyph = self[ord(' ')]
		if not isinstance(glyph, Glyph):
			raise ValueError('No valid reference character found.')
		return glyph

	def create_glyph(self, key: int) -> Glyph:
		g = self.get_reference_char()
		glyph = Glyph(
			# an empty but valid glyph
			f'uni{key:04X}'.encode(), self.get_reference_char().data,
			g.bbX, g.bbY, g.bbW, g.bbH, g.advance, key
		)
		self.glyphs.append(glyph)
		self.glyphs_by_codepoint[key] = glyph
		return glyph

	def save(self, file_name: str) -> None:
		with open(file_name, 'wb') as f:
			writer.write_bdf(self, f)
